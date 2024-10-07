def cli_hal():

    # Standard library import
    from argparse import ArgumentParser, Namespace
    from datetime import datetime
    from pathlib  import Path  
    
    # Third party imports
    import pandas as pd
    
    # Internal import
    from HalApyJson.main import build_hal_df_from_api
    
    parser = ArgumentParser()
    parser.usage = """cli_hal -y <year> -i <institute> -o <output_path> -v <verbose>
    Parses the response of HAL for a publications year and an organisation
    and builds a csv file in the specifyed output path."""

    parser.add_argument('-y',
                        '--year',
                        help='year of the publications',
                        type=str)
    parser.add_argument('-i', '--institute',
                        nargs='?', 
                        help='institute of interest')
    parser.add_argument('-o', '--output',
                        nargs='?', 
                        help='output path for the results')
    parser.add_argument('-v', '--verbose',
                        nargs='?', 
                        help='to activate prints')
    args : Namespace = parser.parse_args()

    if args.output is None:
        output_path = Path.home()
    else:
        output_path = args.output
    
    if args.year is None:
        year = str(datetime.now().year)
    else:
        year = args.year
    
    if args.institute is None:
        institute = "cea"
    else:
        institute = args.institute

    if args.verbose is None:
        verbose = False
    else:
        verbose = args.verbose

    if verbose:
        print(f'Output path is set to: {output_path}')
        print(f'Year is set to: {year}')
        print(f'Institute is set to: {institute}')
        
    hal_df = build_hal_df_from_api(year,institute)
    hal_df.to_excel(Path(output_path)/Path(f'HAL_{institute}_{year}_results.xlsx'), index = False)
    

    
