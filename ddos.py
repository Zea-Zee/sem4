# import requests
# url = "https://fineform.site/"
# thrnom = 12


# while(1):
#     requests.post(url)


from locust import HttpUser, between, task

class WebsiteUser(HttpUser):
    wait_time = between(0.001, 0.002)  # Время между запросами, в секундах
    host = "https://lyceum1-irk.ru"
    @task
    def index_page(self):
        self.client.get("/")  # Замените "/" на путь к вашей странице, которую вы хотите тестировать
