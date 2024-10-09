



async def generate_impl(description: str, private_key_file: str = None, public_key_file: str = None,
                        sign: bool = False, alias: str = None):
    from decentnet.modules.key_util.key_manager import KeyManager
    if sign:
        from decentnet.modules.cryptography.asymetric import AsymCrypt
        private_key, o_public_key = KeyManager.generate_singing_key_pair()
        public_key = AsymCrypt.verifying_key_to_string(o_public_key)
    else:
        private_key, o_public_key = KeyManager.generate_encryption_key_pair()
        public_key = KeyManager.key_to_base64(o_public_key)

    private_key = KeyManager.key_to_base64(private_key)

    if private_key_file:
        with open(private_key_file, 'w') as f:
            f.write(private_key)
    if public_key_file:
        with open(public_key_file, 'w') as f:
            f.write(public_key)
    await KeyManager.save_to_db(private_key, public_key, description, not sign, alias)
