from .convert import run_convert as convert_main
from .covariates import main as covariates_main
from .education import main as education_main
from .families import main as families_main
from .lpr_link import main as lpr_link_main

if __name__ == "__main__":
    convert_main()
    families_main()
    education_main()
    lpr_link_main()
    covariates_main()
