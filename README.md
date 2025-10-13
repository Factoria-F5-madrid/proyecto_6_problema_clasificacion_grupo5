![Encabezado del Proyecto](https://drive.google.com/uc?export=view&id=1Fa6aW9Z4Ah7GLlir2ZzlT_UkM-k8JGNw)

# Predicción de Satisfacción de Clientes Aéreos — You & Airvryone

## Descripción General

Este proyecto fue desarrollado dentro del **Bootcamp de Inteligencia Artificial de Factoría F5**, con el objetivo de construir un sistema capaz de **predecir la satisfacción de los clientes de una aerolínea** a partir de variables relacionadas con el servicio, el tipo de viaje y la experiencia del pasajero.

El sistema integra un modelo de clasificación basado en **XGBoost** dentro de una aplicación **web interactiva** con **FastAPI (backend)** y **React + TailwindCSS (frontend)**, desplegable mediante **Docker**.

---

## Objetivo del Proyecto

Desarrollar una solución de *machine learning* que permita anticipar si un cliente estará **satisfecho o insatisfecho** con su experiencia de vuelo, brindando a las aerolíneas información útil para mejorar sus servicios.

---

## Flujo de Desarrollo

1. **Análisis Exploratorio (EDA)**  
   - Estudio del dataset público de *Airline Passenger Satisfaction (Kaggle)*.  
   - Limpieza, imputación de valores nulos y codificación categórica.  
   - Visualización de correlaciones clave.

2. **Preprocesamiento de Datos**  
   - Escalado de variables numéricas con `MinMaxScaler`.  
   - Balanceo de clases con `SMOTE`.  
   - División en *train/test* (80/20).

3. **Entrenamiento y Selección del Modelo**  
   - Algoritmos evaluados: Logistic Regression, Random Forest, XGBoost.  
   - Métricas: Accuracy, Precision, Recall, F1-score y ROC-AUC.  
   - Modelo final: **XGBoost (F1-score: 0.89, Accuracy: 0.91)**.

4. **Productivización y Despliegue**  
   - Backend con **FastAPI**: endpoint `/predict` que recibe JSON y devuelve predicción.  
   - Frontend en **React + Tailwind** con formulario intuitivo.  
   - Contenedores **Docker** (frontend + backend) orquestados con `docker-compose`.

---

## Arquitectura del Sistema

```plaintext
Frontend (React + Tailwind)
        ↓
Backend (FastAPI + Pydantic)
        ↓
Modelo (XGBoost .pkl)

``` 

---
## Instalación y Ejecución
🔧 Requisitos
- Python ≥ 3.10
- Node.js ≥ 18
- Docker & Docker Compose

---
## Pasos

Clonar el repositorio
```plaintext
git clone https://github.com/<usuario>/<repositorio>.git
cd <repositorio>
``` 
Construir y ejecutar con Docker
```plaintext
docker-compose up --build
``` 
Acceder a la aplicación web
```plaintext
Frontend: http://localhost:3000
Backend API Docs: http://localhost:8000/docs
```
---
## Tecnologías Principales

| Componente      | Tecnología                           |
| --------------- | ------------------------------------ |
| Backend         | FastAPI, Pydantic                    |
| Frontend        | React, TailwindCSS                   |
| Modelo ML       | XGBoost, scikit-learn                |
| Infraestructura | Docker, Docker Compose               |
| Colaboración    | GitHub          Conventional Commits |

---
## Resultados clave 

| Métrica   | Valor |
| --------- | ----- |
| Accuracy  | 0.91  |
| Precision | 0.90  |
| Recall    | 0.88  |
| F1-score  | 0.89  |
| ROC-AUC   | 0.94  |

---
## Variables más influyentes:
- Inflight Service
- Seat Comfort
- Online Boarding
- Cleanliness
---
# Entregables del proyecto: 
(Da click en cada nombre, te llevará al enlace correspondiente)

## 1. Aplicación: 


## 2. Informe Técnico
Puedes consultar el Informe Técnico completo con el detalle del análisis, desarrollo y resultados en el siguiente enlace:

. 📄 Descargar Informe Técnico (PDF)

## 3.  Presentación:
[Presentación comercial y técnica](https://www.canva.com/design/DAG1AK9ch5Q/rnldsVgfWjZABMhU52n23g/edit?utm_content=DAG1AK9ch5Q&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton)


## 4. Git Projects: 

 

## 5. Otros: 
- [Carpeta en la que organizamos entregables](https://drive.google.com/drive/folders/1-uul70XgQp3TDPcD-CMsN2Bbi8kcHG2_?usp=sharing)

Encontrán: 

- Guión
- Fondo de Zoom
- Documento de redacción para informe técnico
- Actas de reunión, enlazadas a Git Project

---

## Equipo
- [Maribel Gutiérrez Ramírez](https://www.linkedin.com/in/maribel-guti%C3%A9rrez-ram%C3%ADrez/)

- [Teo Ramos](https://www.linkedin.com/in/teo-ramos-ruano/)

- [Alfonso Bermúdez](https://www.linkedin.com/in/alfonsobermudeztorres/)

- [Yeder Pimentel](https://www.linkedin.com/in/yeder-pimentel/)


© 2025 — You & Airvryone — Proyecto de Clasificación de Satisfacción de Clientes Aéreos
