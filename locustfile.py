
#locust --host=http://localhost:port-where-server-is-running/ 
#http://localhost:8089/ 

from locust import HttpLocust, TaskSet

# def login(l):
#     l.client.post("/login", {"username":"ellen_key", "password":"education"})

def fit_bounds_kha_outzoom(l):
    l.client.get("api/polygon/fit_bounds/1/30.81665,48.08175,41.36353,51.28941/")

def fit_bounds_kha(l):
    l.client.get("api/polygon/fit_bounds/3/35.92289,49.88977,36.58207,50.08909/")

def index(l):
    l.client.get("")

def update_organizations(l):
    l.client.get("api/update/2016-03-01/organization/")

class UserBehavior(TaskSet):
    tasks = {index:1, 
            # update_organizations:1
            }

    # def on_start(self):
    #     login(self)



class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait=5000
    max_wait=9000
