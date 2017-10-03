import sys

sys.path.insert(0,"../python/")
import search_utils as su
from twitter_crawler import TwitterCrawler

def main(time_frame, max_request_per_time_frame, mongo_coll,search_params, max_id, termination_function):
    tcs = TwitterCrawler(time_frame=time_frame,max_requests=max_request_per_time_frame)
    tcs.connect(mongo_coll)
    tcs.authenticate("../api_key.json")
    tcs.set_search_arguments(search_args=search_params)
    tcs.search_by_query(wait_for=3, current_max_id=max_id, term_func=termination_function)
    tcs.close()

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: <time_frame> <max_request_per_time_frame> <mongo_collection> <max_id>")
    else:
        # crawler parameters
        time_frame = int(sys.argv[1])
        max_request_per_time_frame = int(sys.argv[2])
        mongo_coll = sys.argv[3]
        my_max_id = int(sys.argv[4])
        
        # termination function
        #my_created_at="Thu Aug 17 22:00:00 +0000 2017"
        #def my_time_bound_filter(tweet):
        #    return su.time_bound_filter(tweet, created_at=my_created_at)
        
        #my_since_id = 903184720040783872 # "Thu Aug 31 09:16:32 +0000 2017"
        #my_since_id = 905535688497545216 # approx 2017-09-06
        my_since_id = 907170868396216320 # approx 2017-09-10
        def my_since_id_filter(tweet):
                return su.id_bound_fiter(tweet, since_id=my_since_id)
        
        # search parameters
        selected_keys = ["#usopen", "#Usopen", "#UsOpen", "#USOpen", "#USOPEN", "#usopen17", "#UsOpen17", "#Usopen2017", "#WTA", "#wta", "#ATP", "#atp", "#Tennis", "#tennis", "#tenis", "#Tenis", "@usopen", "@WTA", "@ATPWorldTour"]
        query = " OR ".join(selected_keys)
        search_params = {
            "q":query,
            "result_type":'recent',
            "count":100
        }
        
        # run crawler
        main(time_frame, max_request_per_time_frame, mongo_coll, search_params, my_max_id, termination_function=my_since_id_filter)
        
