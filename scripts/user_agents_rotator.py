
class UserAgent:
    def __init__(self):
        pass

    def set_random_user_agent(self, driver_options):
        from fake_useragent import UserAgent
        ua=UserAgent()
        user_agent={"User-Agent": str(ua.random)}
        driver_options.add_argument(f'user-agent={user_agent}')
        return
