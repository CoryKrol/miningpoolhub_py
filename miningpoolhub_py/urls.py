class Urls:
    def __init__(self):
        self.protocol = 'https://'
        self.base_url = 'miningpoolhub.com/index.php?page=api&action={action}'
        self.coin_pool = '{coin_pool}.'
        self.no_pool_base_url = self.protocol + self.base_url

        # Urls specific to each coins' mining pool
        self.get_block_count = self.protocol + self.coin_pool + self.base_url.format(action='getblockcount')
        self.get_block_stats = self.protocol + self.coin_pool + self.base_url.format(action='getblockstats')
        self.get_blocks_found = self.protocol + self.coin_pool + self.base_url.format(action='getblocksfound')
        self.get_current_workers = self.protocol + self.coin_pool + self.base_url.format(action='getcurrentworkers')
        self.get_dashboard_data = self.protocol + self.coin_pool + self.base_url.format(action='getdashboarddata')
        self.get_difficulty = self.protocol + self.coin_pool + self.base_url.format(action='getdifficulty')
        self.get_estimated_time = self.protocol + self.coin_pool + self.base_url.format(action='getestimatedtime')
        self.get_hourly_hash_rates = self.protocol + self.coin_pool + self.base_url.format(action='gethourlyhashrates')
        self.get_nav_bar_data = self.protocol + self.coin_pool + self.base_url.format(action='getnavbardata')
        self.get_pool_hash_rate = self.protocol + self.coin_pool + self.base_url.format(action='getpoolhashrate')
        self.get_pool_info = self.protocol + self.coin_pool + self.base_url.format(action='getpoolinfo')
        self.get_pool_share_rate = self.protocol + self.coin_pool + self.base_url.format(action='getpoolsharerate')
        self.get_pool_status = self.protocol + self.coin_pool + self.base_url.format(action='getpoolstatus')
        self.get_time_since_last_block = self.protocol + self.coin_pool + self.base_url.format(
            action='gettimesincelastblock')
        self.get_top_contributors = self.protocol + self.coin_pool + self.base_url.format(action='gettopcontributors')
        self.get_user_balance = self.protocol + self.coin_pool + self.base_url.format(action='getuserbalance')
        self.get_user_hash_rate = self.protocol + self.coin_pool + self.base_url.format(action='getuserhashrate')
        self.get_user_share_rate = self.protocol + self.coin_pool + self.base_url.format(action='getusersharerate')
        self.get_user_status = self.protocol + self.coin_pool + self.base_url.format(action='getuserstatus')
        self.get_user_transactions = self.protocol + self.coin_pool + self.base_url.format(action='getusertransactions')
        self.get_user_workers = self.protocol + self.coin_pool + self.base_url.format(action='getuserworkers')
        self.public = self.protocol + self.coin_pool + self.base_url.format(action='public')

        # Info for all mining pools
        self.get_all_user_balances = self.no_pool_base_url.format(action='getuserallbalances')
        self.get_auto_switching_and_profits_statistics = \
            self.no_pool_base_url.format(action='getautoswitchingandprofitsstatistics')
        self.get_mining_profit_and_statistics = self.no_pool_base_url.format(action='getminingandprofitsstatistics')

    def base_url(self):
        return self.base_url

    def get_block_count_url(self, pool):
        return self.get_block_count.format(coin_pool=pool)

    def get_block_stats_url(self, pool):
        return self.get_block_stats.format(coin_pool=pool)

    def get_blocks_found_url(self, pool):
        return self.get_blocks_found.format(coin_pool=pool)

    def get_current_workers_url(self, pool):
        return self.get_current_workers.format(coin_pool=pool)

    def get_dashboard_data_url(self, pool):
        return self.get_dashboard_data.format(coin_pool=pool)

    def get_difficulty_url(self, pool):
        return self.get_difficulty.format(coin_pool=pool)

    def get_estimated_time_url(self, pool):
        return self.get_estimated_time.format(coin_pool=pool)

    def get_hourly_hash_rates_url(self, pool):
        return self.get_hourly_hash_rates.format(coin_pool=pool)

    def get_nav_bar_data_url(self, pool):
        return self.get_nav_bar_data.format(coin_pool=pool)

    def get_pool_hash_rate_url(self, pool):
        return self.get_pool_hash_rate.format(coin_pool=pool)

    def get_pool_info_url(self, pool):
        return self.get_pool_info.format(coin_pool=pool)

    def get_pool_share_rate_url(self, pool):
        return self.get_pool_share_rate.format(coin_pool=pool)

    def get_pool_status_url(self, pool):
        return self.get_pool_status.format(coin_pool=pool)

    def get_time_since_last_block_url(self, pool):
        return self.get_time_since_last_block.format(coin_pool=pool)

    def get_top_contributors_url(self, pool):
        return self.get_top_contributors.format(coin_pool=pool)

    def get_user_balance_url(self, pool):
        return self.get_user_balance.format(coin_pool=pool)

    def get_user_hash_rate_url(self, pool):
        return self.get_user_hash_rate.format(coin_pool=pool)

    def get_user_share_rate_url(self, pool):
        return self.get_user_share_rate.format(coin_pool=pool)

    def get_user_status_url(self, pool):
        return self.get_user_status.format(coin_pool=pool)

    def get_user_transactions_url(self, pool):
        return self.get_user_transactions.format(coin_pool=pool)

    def get_user_workers_url(self, pool):
        return self.get_user_workers.format(coin_pool=pool)

    def public_url(self, pool):
        return self.public.format(coin_pool=pool)

    def get_all_user_balances_url(self):
        return self.get_all_user_balances

    def get_auto_switching_and_profits_statistics_url(self):
        return self.get_auto_switching_and_profits_statistics

    def get_mining_profit_and_statistics_url(self):
        return self.get_mining_profit_and_statistics
