import java.io.File;
import java.nio.charset.StandardCharsets;
import java.util.Arrays;
import java.util.Base64;

/**
 * @author Kunal Mukherjee
 * @netid kxm180046
 * @email kxm180046@utdallas.edu
 */
public class EFS extends Utility{

    public EFS(Editor e)
    {
        super(e);
        set_username_password();
    }

    // global var for file
    public File nw_folder;

    // helper function to copy bytes
    public byte [] copybytes(String s, byte [] d){

        // copy the content from a string to a byte
        for (int i = 0; i < s.length(); i++){

            if (i <= 128)
                d[i] = s.getBytes(StandardCharsets.UTF_8)[i];;
        }

        return d;
    }

    // takes an arbotary string and makes it 128by
    public byte[] correctLenMaker(String str, byte[] str_by, String str_name) {
        // check to see if username and password is 128 bytes
        if (str.length() > 128) {
            str_by = copybytes(str.substring(0, 128), str_by);
        } else {
            str_by = copybytes(str, str_by);
        }

        /*// debug
        System.out.println(str_name + " set to correct length");
        System.out.println(
                byteArray2String(str_by) + " "
                        + "len:" + byteArray2String(str_by).length() + " "
                        + "set");*/

        return str_by;
    }

    // get the block content
    public byte[] getBlockContent(String file_name, int blockint) throws Exception {
        // get the meta data file
        File file = new File(file_name);
        File meta = new File(file, Integer.toString(blockint));

        // copy byte[] from the file
        return read_from_file(meta);
    }

    // get the IV_128by from file
    public byte[] getIV_128by(byte[] block0){

        // get the IV byte[] from file
        byte[] IV_172by = new byte[172];
        System.arraycopy(block0,128, IV_172by,0, 172);

        byte[] IV_ctr_128by = Base64.getDecoder().decode(IV_172by);

        // debug
        //System.out.println("IV found:" + IV_ctr_128by + " len: " + IV_ctr_128by.length);
        return IV_ctr_128by;
    }

    // get the password_128by from file
    public byte[] getPassword_128by(byte[] block0){

        // get the password byte[] from file
        byte[] saltPassBlockFile_172byte = new byte[172];
        System.arraycopy(block0,300,saltPassBlockFile_172byte,0, 172);

        byte[]  password_block_128by = Base64.getDecoder().decode(saltPassBlockFile_172byte);

        // debug
        //System.out.println("Password found:" + password_block_128by + " len: " + password_block_128by.length);
        return password_block_128by;
    }

    // from a 128by pt -> 128by Enc_ct
    public void AESEncrbufferMaker(byte[] pass_128by,
                                   byte[] IV_ctr_128by,
                                   byte[] src,
                                   byte[] dst) throws Exception {

        // varible for counter
        int ctr = 0;
        for (int i = 0; i < src.length; i+= 16){
            // plain text to encrypt
            byte[] pt_16byte = new byte[16];
            // create the key
            byte[] key_16byte = new byte[16];

            // copy the plaintext
            System.arraycopy(src, i, pt_16byte, 0, 16);

            // password 8 byte
            System.arraycopy(pass_128by, i, key_16byte, 0, 8);
            // IV 8 bytes
            System.arraycopy(IV_ctr_128by, i, key_16byte, 8, 7);
            // add the counter
            key_16byte[15] = (byte) (IV_ctr_128by[i+8]+ctr);

            // encrypt the block
            System.arraycopy(encript_AES(pt_16byte, key_16byte), 0,
                    dst, i, encript_AES(pt_16byte, key_16byte).length);

            // increment counter
            ctr++;
        }
    }

    // from a 128by Enc_ct -> 128by pt
    public void AESDecrbufferMaker(byte[] pass_128by,
                                   byte[] IV_ctr_128by,
                                   byte[] src,
                                   byte[] dst) throws Exception {

        int ctr = 0;
        for (int i = 0; i < src.length; i+= 16){
            // ciphertext to decrypt and key
            byte[] ct_16byte = new byte[16];
            byte[] key_16byte = new byte[16];

            // copy the ciphertext
            System.arraycopy(src, i, ct_16byte, 0, 16);

            // password 8 byte
            System.arraycopy(pass_128by, i, key_16byte, 0, 8);
            // IV 8 bytes
            System.arraycopy(IV_ctr_128by, i, key_16byte, 8, 7);
            // add the counter
            key_16byte[15] = (byte) (IV_ctr_128by[i+8]+ctr);

            // decrypt the block
            System.arraycopy(decript_AES(ct_16byte, key_16byte), 0,
                    dst, i, decript_AES(ct_16byte, key_16byte).length);

            // increment the counter
            ctr++;
        }
    }

    // build 1024 byte blocks
    public void buildEncryptedBlocks(String file_name,
                                     int block_i ,
                                     byte[] IV_ctr_128by,
                                     byte[] password_128by) throws Exception {

        File file = new File(file_name);
        // get to file
        File meta = new File(file, Integer.toString(block_i));
        // if file doesn't exists then only create and write
        if (!meta.exists()) {

            byte[] block_1024by = new byte[1024];

            for (int i = 0; i < 1024; i += 128) {
                // create the src and dst byte array
                byte[] src_128by = new byte[128];
                byte[] dst_128by = new byte[128];

                // copy the array to src buffer
                System.arraycopy(block_1024by, i, src_128by, 0, 128);

                // encrypt the buffer
                AESEncrbufferMaker(password_128by, IV_ctr_128by, src_128by, dst_128by);

                // copy the encyp buffer to array
                System.arraycopy(dst_128by, 0, block_1024by, i, 128);

            }

            String block_content = Base64.getEncoder().encodeToString(block_1024by);
            String block_content_1024by = block_content.substring(0, 1024);

            save_to_file(block_content_1024by.getBytes(StandardCharsets.UTF_8), meta);
        }

        //System.out.println("Finished writing encrypted buffer to file");
    }

    // get the hash(password||salt) from password
    public byte[] getHashPassword_128by(String pass_word, byte[] IV_ctr_128by) throws Exception {

        // generated the password||salt
        // create the H(password||salt) -> SHA256[Password||IV]
        // create the 128 byte variable to hold the password
        byte[] password_128by = new byte[128];
        password_128by = correctLenMaker(pass_word, password_128by, "password");

        byte[] pass_salt = new byte[password_128by.length + IV_ctr_128by.length];
        System.arraycopy(password_128by, 0, pass_salt, 0, password_128by.length);
        System.arraycopy(IV_ctr_128by, 0, pass_salt, password_128by.length, IV_ctr_128by.length);

        // get the hash(password||salt)
        byte [] hash_salt_pass_256bit = hash_SHA256(pass_salt);

        byte[] hash_salt_pass_128by = new byte[128];
        System.arraycopy(hash_salt_pass_256bit,0, hash_salt_pass_128by,0,hash_salt_pass_256bit.length);

        return hash_salt_pass_128by;
    }

    // helper function to create the 256bit HMAC
    private byte[] getHMAC_256bit(byte[] password_128by, byte[] IV_ctr_128by, String message) throws Exception {
        // HMAC[M] = H(K || H(K || M))
        // creating K_temp
        byte[] K_temp = new byte[password_128by.length + IV_ctr_128by.length];
        System.arraycopy(password_128by, 0, K_temp, 0, password_128by.length);
        System.arraycopy(IV_ctr_128by, 0, K_temp, password_128by.length, IV_ctr_128by.length);

        byte[] k_256bit = hash_SHA256(K_temp);

        // create opad
        byte[] opad = new byte[32];
        // create ipad
        byte[] ipad = new byte[32];

        for (int i = 0; i < (256/8); i++){
            opad[i] = (byte) (0x5c ^ k_256bit[i]);
            ipad[i] = (byte) (0x36 ^ k_256bit[i]);
        }

        byte[] message_by = message.getBytes(StandardCharsets.UTF_8);

        // inside message hash
        byte[] message_inside = new byte[ipad.length + message_by.length];
        System.arraycopy(ipad, 0, message_inside, 0, ipad.length);
        System.arraycopy(message_by, 0, message_inside, ipad.length, message_by.length);
        byte[] hash_message_inside = hash_SHA256(message_inside);

        // outside message hash
        byte[] message_outside = new byte[opad.length + hash_message_inside.length];
        System.arraycopy(opad, 0, message_outside, 0, opad.length);
        System.arraycopy(hash_message_inside, 0, message_outside, opad.length, hash_message_inside.length);
        byte[] HMAC_256bit = hash_SHA256(message_outside);
        return HMAC_256bit;
    }

    // function to get the HMAC of a message
    public byte[] getAES_HMAC_128by(byte[] password_128by, byte[] IV_ctr_128by, String message) throws Exception {

        byte[] HMAC_256bit = getHMAC_256bit(password_128by, IV_ctr_128by, message);

        // put the 256 bit hash -> 128 byte
        byte[] HMAC_128by = new byte[128];
        // create a 128 byte HMAC
        System.arraycopy(HMAC_256bit, 0, HMAC_128by, 0, HMAC_256bit.length);

        // encrypt the 128 byte HMAC
        byte[] AES_MAC_128by = new byte[128];
        AESEncrbufferMaker(password_128by, IV_ctr_128by, HMAC_128by, AES_MAC_128by);
        return AES_MAC_128by;
    }

    // function that returns the length of a block
    public int getLength(byte[] block0, byte[] IV_ctr_128by, byte[] password_128by) throws Exception {

        // get the encoded encrpted length from block
        byte[] length_172by = new byte[172];
        System.arraycopy(block0, 644, length_172by, 0, 172);

        // get the decoded encrypted length from block
        byte[] enc_length_128by = Base64.getDecoder().decode(length_172by);

        // debug
        //System.out.println("length found:" + enc_length_128by + " len: " + enc_length_128by.length);

        // get the length decrpted length
        byte[] length_128by = new byte[128];
        AESDecrbufferMaker(password_128by, IV_ctr_128by, enc_length_128by, length_128by);

        // convert the decrypted length to string
        String leng = new String(length_128by, StandardCharsets.UTF_8).replace("\u0000", "");

        // parse the int from the string
        int lengt = Integer.parseInt(leng);
        //System.out.println("len: " + lengt);
        return lengt;
    }

    // function to see if password match
    public boolean doesPasswordMatch(String file_name, String pass_word) throws Exception {

        // get the block0 content
        byte[] block0 = getBlockContent(file_name, 0);
        // get the IV byte[] from file
        byte[] IV_ctr_128by = getIV_128by(block0);
        // get the password from file
        byte [] saltPassBlockFile = getPassword_128by(block0);

        // get the hashed password from string
        byte[] hash_salt_pass_128by = getHashPassword_128by(pass_word, IV_ctr_128by);

        return Arrays.equals(hash_salt_pass_128by, saltPassBlockFile);
    }

    // write the message to childBlock and HMAC parentBlock
    public void writeMessageBlock(String file_name,
                                  String message,
                                  byte[] IV_ctr_128by,
                                  byte[] password_128by,
                                  int starting_position
                                  ) throws Exception {

        // part A: update the length
        // get the length from the string
        String length = Integer.toString(message.length());

        // convert length -> padded length
        byte[] length_128by = new byte[128];
        length_128by = correctLenMaker(length, length_128by, "length");

        // encrypted padded length
        byte[] AES_length_128by = new byte[128];
        AESEncrbufferMaker(password_128by, IV_ctr_128by, length_128by, AES_length_128by);

        // update length meta data in block0
        byte[] block0 = getBlockContent(file_name, 0).clone();

        // encode the encrypted padded length
        System.arraycopy(Base64.getEncoder().encode(AES_length_128by), 0,
                block0, 644, 172);

        // write to file
        // get the meta data file
        File file = new File(file_name);

        // write to file
        File meta0 = new File(file, Integer.toString(0));
        save_to_file(block0, meta0);
        //System.out.println("Finished writing length to block0");

        // part B:

        // get the number of blocks needs
        int num_block = (message.length() / 128) + 1;

        // build blocks
        for (int i = 1; i <= num_block; i++){
            buildEncryptedBlocks(file_name, i, IV_ctr_128by, password_128by);
        }

        // for the updated block
        for (int parent = starting_position / 128; parent < num_block; parent++) {
            String message_block = "";

            // create the block message blocks
            if ((parent * 128) + 128 < message.length()) {
                message_block = message.substring(parent * 128, (parent * 128) + 128);
            } else {
                message_block = message.substring(parent * 128, message.length());
            }

            byte[] blockBuffer_128by = new byte[128];
            blockBuffer_128by = correctLenMaker(message_block, blockBuffer_128by, "message");

            byte[] AES_blockBuffer_128by = new byte[128];
            AESEncrbufferMaker(password_128by, IV_ctr_128by, blockBuffer_128by, AES_blockBuffer_128by);

            byte[] currentBlockContent = getBlockContent(file_name, parent + 1);
            System.arraycopy(Base64.getEncoder().encode(AES_blockBuffer_128by), 0,
                    currentBlockContent, 0, Base64.getEncoder().encode(AES_blockBuffer_128by).length);
            // write to file
            File meta1 = new File(file, Integer.toString(parent + 1));
            save_to_file(currentBlockContent, meta1);
            //System.out.println("Finished writing to child file");

            // update block1 meta data in block0
            // copy byte[] from the file
            byte[] block1 = getBlockContent(file_name, parent).clone();
            //System.out.println(block1.length);

            // get 256 bit hash of message
            byte[] AES_MAC_128by = getAES_HMAC_128by(password_128by, IV_ctr_128by, message_block);

            // copy the encoded encrypted MAC to block0
            System.arraycopy(Base64.getEncoder().encode(AES_MAC_128by), 0,
                    block1, 472, 172);

            // write to file
            File meta_parent = new File(file, Integer.toString(parent));
            save_to_file(block1, meta_parent);
            //System.out.println("Finished writing to file");
        }
    }

    /**
     * Steps to consider... <p>
     *  - add padded username and password salt to header <p>
     *  - add password hash and file length to secret data <p>
     *  - AES encrypt padded secret data <p>
     *  - add header and encrypted secret data to metadata <p>
     *  - compute HMAC for integrity check of metadata <p>
     *  - add metadata and HMAC to metadata file block <p>
     */
    @Override
    public void create(String file_name, String user_name, String pass_word) throws Exception {

        // variable to hold the contents that will be written
        String metadataWriter = "";

        // create the variable to hold the username
        byte[] username_128by = new byte[128];

        // convert String -> char [128] for username
        username_128by = correctLenMaker(user_name, username_128by, "username");
        // fill up the first block
        metadataWriter += new String(username_128by, StandardCharsets.UTF_8);
        //System.out.println("username len: " + username_128by.length + " mdWriter: " + metadataWriter.length());

        // generate the IV
        // create other variables to hold other list
        byte[] IV_ctr_128by =  secureRandomNumber(128);
        //debug
        //System.out.println("IV set:" + IV_ctr_128by + " len: " + IV_ctr_128by.length);
        // write the IV to metadata
        metadataWriter += Base64.getEncoder().encodeToString(IV_ctr_128by);
        //System.out.println("IV: " + metadataWriter.length());

        // create the H(password||salt) -> SHA256[Password||IV]
        // create the 128 byte variable to hold the password
        byte[] password_128by = new byte[128];
        password_128by = correctLenMaker(pass_word, password_128by, "password");

        // generated the password||salt
        byte[] pass_salt = new byte[password_128by.length + IV_ctr_128by.length];
        System.arraycopy(password_128by, 0, pass_salt, 0, password_128by.length);
        System.arraycopy(IV_ctr_128by, 0, pass_salt, password_128by.length, IV_ctr_128by.length);

        // get the hash(password||salt)
        byte [] hash_salt_pass_256bit = hash_SHA256(pass_salt);

        byte[] hash_salt_pass_128by = new byte[128];
        System.arraycopy(hash_salt_pass_256bit,0, hash_salt_pass_128by,0,hash_salt_pass_256bit.length);

        metadataWriter += Base64.getEncoder().encodeToString(hash_salt_pass_128by);
        //System.out.println("salted password: " + metadataWriter.length());

        // get 256 bit hash of message
        String message = "";
        byte[] AES_MAC_128by = getAES_HMAC_128by(password_128by, IV_ctr_128by, message);

        // add the hash to toWrite
        metadataWriter += Base64.getEncoder().encodeToString(AES_MAC_128by);
        //System.out.println("AES MAC size: " + metadataWriter.length());

        // encrypt the length
        String length = Integer.toString(message.length());
        byte[] length_128by = new byte[128];
        length_128by = correctLenMaker(length, length_128by, "length");

        byte[] AES_length_128by = new byte[128];
        AESEncrbufferMaker(password_128by, IV_ctr_128by, length_128by, AES_length_128by);

        metadataWriter += Base64.getEncoder().encodeToString(AES_length_128by);
        //System.out.println("AES length size: " + metadataWriter.length());

        //padding to 1024
        while (metadataWriter.length()+2< Config.BLOCK_SIZE) {
            int rand_iv = Math.abs(secureRandomNumber(1)[0]) % 128;
            metadataWriter += IV_ctr_128by[rand_iv];
        }
        //System.out.println("file1 content created: " + metadataWriter.length());

        // create a new folder
        nw_folder = new File(file_name);
        nw_folder.mkdirs();

        // create a new file 0
        File meta = new File(nw_folder, "0");
        //System.out.println("Folder and subfolder created");

        save_to_file(metadataWriter.getBytes(StandardCharsets.UTF_8), meta);
        //System.out.println("Finished writing to file");

        //System.out.println("saved block0");
    }

    /**
     * Steps to consider...:<p>
     *	- verify password <p>
     *  - check check if requested starting position and length are valid <p>
     *  - ### main procedure for update the encrypted content ### <p>
     *  - compute new HMAC and update metadata
     */
    @Override
    public void write(String file_name, int starting_position, byte[] content, String pass_word) throws Exception {

        // get the block0 content
        byte[] block0 = getBlockContent(file_name, 0);
        // get the IV byte[] from file
        byte[] IV_ctr_128by = getIV_128by(block0);
        // get the password from file
        byte[] password_128by = getPassword_128by(block0);

        if (doesPasswordMatch(file_name, pass_word)){
            //System.out.println("***Password match***");

            String message;
            int len;

            try{
                 len = length(file_name,pass_word);
            } catch (Exception e){
                len = 0;
            }

            String new_message = new String(content, StandardCharsets.UTF_8);

            if (len > 0){
                // get the message from file
                byte [] message_f =  read(file_name,0, length(file_name, pass_word), pass_word);

                // get the message string from file
                String message_f_str = new String(message_f, StandardCharsets.UTF_8);

                if (new_message.length() >=
                        message_f_str.substring(starting_position, message_f_str.length()).length()){

                    // update the message string
                    message = message_f_str.substring(0, starting_position) +  new_message;
                }else{
                    // update the message string
                    message = message_f_str.substring(0, starting_position) +  new_message
                            + message_f_str.substring(starting_position+new_message.length(), message_f_str.length());
                }

            } else {
                // put the message in a block 1
                // convert the message in string
                message = new_message;
            }

            // write the new message to block
            writeMessageBlock(file_name, message, IV_ctr_128by, password_128by, starting_position);

        }else{
            //System.out.println("Password not match");
            throw new PasswordIncorrectException();
        }

    }

    /**
     * Steps to consider...:<p>
     *  - verify password <p>
     *  - check check if requested starting position and length are valid <p>
     *  - decrypt content data of requested length 
     */
    @Override
    public byte[] read(String file_name, int starting_position, int len, String pass_word) throws Exception {

        // get the block0 content
        byte[] block0 = getBlockContent(file_name, 0);
        // get the IV byte[] from file
        byte[] IV_ctr_128by = getIV_128by(block0);
        // get the password from file
        byte [] password_128by = getPassword_128by(block0);

        // read the file only if it has integrity
        if (!check_integrity(file_name, pass_word)) {
            javax.swing.JOptionPane.showMessageDialog(null, "The file has been modified");
        }
        else {

            // check to see if password match
            if (doesPasswordMatch(file_name, pass_word)) {
                int lengt = getLength(block0, IV_ctr_128by, password_128by);

                // get the number of blocks needs
                int num_block = (lengt / 128) + 1;

                // get the chosen sub string
                String chosen_file_message = "";
                StringBuilder tmp_pt = new StringBuilder();

                for (int i = 1; i <= num_block; i++){
                    // put the message in a block 1
                    byte[] block1 = getBlockContent(file_name, i);

                    // get the encoded encry_message
                    byte[] encr_mess_172by = new byte[172];
                    System.arraycopy(block1, 0, encr_mess_172by, 0, 172);

                    // copy decoded encrypted byte[] from the file
                    byte[] encr_mesg_128by = Base64.getDecoder().decode(encr_mess_172by);

                    byte [] AES_blockBuffer_128by = new byte [128];

                    // get the decrypted decoded message data
                    AESDecrbufferMaker(password_128by, IV_ctr_128by, encr_mesg_128by, AES_blockBuffer_128by);

                    tmp_pt.append(new String(AES_blockBuffer_128by, StandardCharsets.UTF_8).replace("\u0000", ""));

                }

                // get the chosen sub string
                chosen_file_message = tmp_pt.substring(starting_position, starting_position+len);

                return chosen_file_message.getBytes(StandardCharsets.UTF_8);

            } else {
                //System.out.println("Password not match");
                throw new PasswordIncorrectException();
            }

        }
        return "".getBytes(StandardCharsets.UTF_8);
    }

    /**
     * Steps to consider...:<p>
     *  - verify password <p>
     *  - check the equality of the computed and stored HMAC values for metadata and physical file blocks<p>
     */
    @Override
    public boolean check_integrity(String file_name, String pass_word) throws Exception {
        // get the block0 content
        byte[] block0 = getBlockContent(file_name, 0);
        // get the IV byte[] from file
        byte[] IV_ctr_128by = getIV_128by(block0);
        // get the password from file
        byte [] password_128by = getPassword_128by(block0);

        // password matched
        if (doesPasswordMatch(file_name, pass_word)){

            //System.out.println("***Password match***");

            // get the num blocks
            int len = length(file_name,pass_word);

            int num_blocks = (len / 128) + 1;

            for (int i = 0; i < num_blocks; i ++){

                // get the parent block
                byte[] block = getBlockContent(file_name, i);

                // get the encoded encrypted padded HMAC
                byte[] hmac_172by = new byte[172];
                System.arraycopy(block, 472, hmac_172by, 0, 172);

                // get the decoded encrypted padded MAC
                byte[] enc_hmac_128by = Base64.getDecoder().decode(hmac_172by);

                // debug
                //System.out.println("length found:" + enc_hmac_128by + " len: " + enc_hmac_128by.length);

                // get the decrypted decoded padded MAC
                byte[] hmac_128by = new byte[128];
                AESDecrbufferMaker(password_128by, IV_ctr_128by, enc_hmac_128by, hmac_128by);

                // get the decrypted decoded unpadded MAC
                byte[] mac_256bit_file = new byte[32];
                System.arraycopy(hmac_128by, 0, mac_256bit_file, 0, 32);
                //System.out.println("len: " + mac_256bit_file.toString());

                // get the message from block i
                byte[] block1 = getBlockContent(file_name, i+1);

                // get the encrypted encoded message
                byte[] encr_mess_172by = new byte[172];
                System.arraycopy(block1, 0, encr_mess_172by, 0, 172);

                // cget the encrypted decoded message
                byte[] encr_mesg_128by = Base64.getDecoder().decode(encr_mess_172by);

                // get the unencrypted decoded message
                byte[] AES_blockBuffer_128by = new byte[128];
                AESDecrbufferMaker(password_128by, IV_ctr_128by, encr_mesg_128by, AES_blockBuffer_128by);

                // get the message
                String tmp_pt = new String(AES_blockBuffer_128by, StandardCharsets.US_ASCII).replace("\u0000", "");

                // get 256 bit hash of message
                byte[] MAC_256bit = getHMAC_256bit(password_128by, IV_ctr_128by, tmp_pt);

                // compare the hash from file and the hash of the message
                if (!Arrays.equals(MAC_256bit, mac_256bit_file)){
                    return false;
                }

            }

            return true;

        }else{
            //System.out.println("Password not match");
            throw new PasswordIncorrectException();
        }
    }

    /**
     * Steps to consider...:<p>
     *  - get password, salt then AES key <p>
     *  - decrypt password hash out of encrypted secret data <p>
     *  - check the equality of the two password hash values <p>
     *  - decrypt file length out of encrypted secret data
     */
    @Override
    public int length(String file_name, String pass_word) throws Exception {

        // get the block0 content
        byte[] block0 = getBlockContent(file_name, 0);
        // get the IV byte[] from file
        byte[] IV_ctr_128by = getIV_128by(block0);
        // get the password from file
        byte [] password_128by = getPassword_128by(block0);

        if (doesPasswordMatch(file_name, pass_word)){

            return getLength(block0, IV_ctr_128by, password_128by);

        }else{
            //System.out.println("Password not match");
            throw new PasswordIncorrectException();
        }

    }

    /**
     * Steps to consider... <p>
     *  - verify password <p>
     *  - truncate the content after the specified length <p>
     *  - re-pad, update metadata and HMA C <p>
     */
    @Override
    public void cut(String file_name, int length_str, String pass_word) throws Exception {

        // call read and get the message length
        int len = length(file_name, pass_word);
        byte [] message_b = read(file_name,0, len, pass_word);

        // truncate the message length
        String message_str = new String(message_b, StandardCharsets.UTF_8);
        String message = message_str.substring(0, length_str);

        // get the block0 content
        byte[] block0 = getBlockContent(file_name, 0);
        // get the IV byte[] from file
        byte[] IV_ctr_128by = getIV_128by(block0);
        // get the password from file
        byte[] password_128by = getPassword_128by(block0);

        // write the new message to block
        writeMessageBlock(file_name, message, IV_ctr_128by, password_128by, 0);
    }

    /**
     * Steps to consider... <p>
     *  - check if metadata file size is valid <p>
     *  - get username from metadata <p>
     */
    @Override
    public String findUser(String file_name) throws Exception {

        // get the block0
        byte[] block0 = getBlockContent(file_name, 0);

        // get the username
        byte[] userBlock = new byte[128];
        System.arraycopy(block0,0,userBlock,0, 128);

        // convert the byte[] to string
        String user = byteArray2String(userBlock);
        //System.out.println("User: " + user);

        // return the user
        return user;
    }

}
