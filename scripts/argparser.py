import argparse



class ArgParser:
    def __init__(self):
        pass
    
    def likes_scraper_read_input(self):

        parser = argparse.ArgumentParser('Instagram likes scraper')
        parser._action_groups.pop()
        required = parser.add_argument_group('required arguments')
        optional = parser.add_argument_group('optional arguments')

        required.add_argument("-u", "--username", help="IG username", required=True)
        required.add_argument("-p", "--password", help="IG password", required=True)
        required.add_argument("-t", "--target_post", help="Target IG post url", required=True)

        return parser.parse_args()