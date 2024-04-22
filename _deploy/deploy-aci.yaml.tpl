apiVersion: 2021-10-01
name: films_predict
properties:
  containers:
  - name: web-api
    properties:
      image: acrfilm.azurecr.io/api
      resources:
        requests:
          cpu: 1
          memoryInGb: 1.5
      ports:
        - port: 8001
  
  - name: web-django
    properties:
      image: acrfilm.azurecr.io/django
      resources:
        requests:
          cpu: 2
          memoryInGb: 3
      ports:
        - port: 80
      environmentVariables:
        - name: "FILM_DB"
          value: "films_db"
        - name: "FILM_USER"
          value: ""
        - name: "FILM_PWD"
          value: ""
        - name: "AZURE_URL"
          value: ""
        - name: "AZURE_USER"
          value: ""
        - name: "AZURE_PWD"
          value: ""
        - name: "DEBUG"
          value: "True"
        - name: "SECRET_KEY"
          value: ""
  osType: Linux
  ipAddress:
    type: Public
    ports:
    - protocol: tcp
      port: 80
  imageRegistryCredentials: # Credentials to pull a private image
  - server: "acrfilm.azurecr.io"
    username: ""
    password: ""