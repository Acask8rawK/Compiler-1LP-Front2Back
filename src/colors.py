class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    @staticmethod
    def print_header(text):
        print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*50}")
        print(f" {text}")
        print(f"{'='*50}{Colors.ENDC}")

    @staticmethod
    def print_success(text):
        print(f"{Colors.GREEN}{Colors.BOLD}✅ [SUCCESS] {text}{Colors.ENDC}")

    @staticmethod
    def print_error(text):
        print(f"{Colors.FAIL}{Colors.BOLD}❌ [ERROR] {text}{Colors.ENDC}")

    @staticmethod
    def print_warning(text):
        print(f"{Colors.WARNING}⚠️  [WARNING] {text}{Colors.ENDC}")

    @staticmethod
    def print_info(text):
        print(f"{Colors.CYAN}ℹ️  {text}{Colors.ENDC}")