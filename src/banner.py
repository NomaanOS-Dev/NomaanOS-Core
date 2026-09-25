def render_banner():
    banner_art = r"""
  _  _                     _    ___  ____     ____          
 | \| |___ _ __  __ _ _ _ /_\  / __|/ __|   / __ \ ___ _ _ 
 | .` / _ \ '  \/ _` | ' \ _ \ \__ \\__ \  | ffff |/ -_) '_|
 |_|\_\___/_|_|_\__,_|_||_/_/ \_|___/___/   \____/ \___|_|  
    """
    print("\033[1;36m" + banner_art + "\033[0m")
    print("\033[1;32m[+] Sovereign AI Stack (SAS) - Enterprise Security Kernel v6.0\033[0m")
    print("\033[1;33m[+] Architect & Founder: Nomaan Khan | Scholar @ IHFC-IITD\033[0m")
    print("\033[1;35m[+] Status: Enclave Hardened & Cryptographically Verified\033[0m\n")

if __name__ == "__main__":
    render_banner()
