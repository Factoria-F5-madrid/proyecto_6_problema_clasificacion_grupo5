![Encabezado del Proyecto](https://drive.google.com/uc?export=view&id=1Fa6aW9Z4Ah7GLlir2ZzlT_UkM-k8JGNw)

# Predicción de Satisfacción de Clientes Aéreos — You & Airvryone

## Descripción General

Este proyecto fue desarrollado dentro del **Bootcamp de Inteligencia Artificial de Factoría F5**, con el objetivo de construir un sistema capaz de **predecir la satisfacción de los clientes de una aerolínea** a partir de variables relacionadas con el servicio, el tipo de viaje y la experiencia del pasajero.

El sistema integra un modelo de clasificación basado en **Random Forest GridSearchCV** dentro de una aplicación **web interactiva** con **FastAPI (backend)** y **React + TailwindCSS (frontend)**.

---

## Objetivo del Proyecto

Desarrollar una solución de *machine learning* que permita anticipar si un cliente estará **satisfecho o insatisfecho** con su experiencia de vuelo, brindando a las aerolíneas información útil para mejorar sus servicios.

---

## Flujo de Desarrollo

1. **Análisis Exploratorio (EDA)**  (`01_EDA-preprocessing.ipynb`)
	- Estudio del dataset público de *Airline Passenger Satisfaction (Kaggle)*.  
    - Limpieza, imputación de valores nulos y codificación categórica.  
    - Visualización de correlaciones clave.

2. **Preprocesamiento de Datos**  (`02_dataset-split.ipynb`)
	- Creación de conjuntos train y test (80/20).
	- Generación de versiones escaladas (para modelos basados en distancia) y no escaladas (para árboles).
 
3. **Entrenamiento y Selección del Modelo**  
    - Cada algoritmo se trabajó en un notebook independiente, aplicando:
	- Modelo base (baseline).
	- Validación cruzada (k-folds).
	- Optimización con GridSearchCV, RandomizedSearchCV y Optuna.

	- Modelos analizados (notebooks `03_<algoritrmo>.ipynb`):
	   - Regresión Logística
	   - K-Nearest Neighbors (KNN)
	   - Árbol de Decisión
	   - Random Forest
	   - XGBoost

	- Comparación de modelos (notebook `04_ModelComparison.ipynb`) con métricas estandarizadas:
	   - Consolidación de métricas: Accuracy, Precision, Recall, F1-score y ROC-AUC.
	   - Cálculo de un Mean Score global y ranking final.
	   - Selección del mejor modelo.

	- Evaluación final (notebook `05_Test-Set-Final.ipynb`) con el mejor modelo
	   - Test sobre datos no vistos.
	   - Obtención de métricas finales, matriz de confusión y curva ROC.

	- Reentrenamiento con el mejor modelo y análisis de variables (notebook `06_FeatureImportanceSelection.ipynb`) para producción.
	   - Cálculo de feature importance.
	   - Entrenamiento del modelo ganador con las 10 variables más influyentes.
	   - Exportación del modelo final para producción.

   - Se entrenan varios modelos supervisados, cada uno en su notebook correspondiente:
      -  Logistic Regression
      -  K-Nearest Neighbors (KNN)
      -  Decision Tree
      -  Random Forest
      -  XGBoost
	-  Cada modelo se entrena en tres fases: baseline, GridSearchCV y Optuna tuning.

4. **Comparación resultados** 
	- Se comparan los resultados mediante un notebook de comparación global.

5. **Test Set Final**
	-  El mejor modelo se evalúa en el Test Set Final 
	
6. **Reentrenamiento del mejor modelo seleccionado**
	- Se reentrena con las 10 variables más importantes para optimizar la interpretabilidad.


## Resultados clave 

![Comparativa de métricas](../reports/figures/ranking_modelos.png)

## Resultados Principales:
Tras comparar el rendimiento de todos los algoritmos:
- El `Random Forest` optimizado con `GridSearchCV` obtiene el mejor rendimiento global, con una media de métricas (Mean Score) de `0.956`, superando a los demás modelos.
- El XGBoost con Optuna logra valores muy competitivos, especialmente en F1-score y ROC-AUC, pero con una ligera menor estabilidad.
- Las 10 variables más relevantes fueron determinadas mediante feature importance, y con ellas se reentrenó el modelo final para producción.


## Justificación sobre la elección de la elección del mejor modelo:  

Aunque XGBoost (Optuna) obtuvo el Mean Score más alto, **el modelo seleccionado como ganador** fue **Random Forest (GridSearchCV)**, debido a su:
- Mayor **estabilidad** entre validaciones cruzadas,
- **Mejor rendimiento** en el conjunto de test (generalización),
- Y una **interpretabilidad** más clara para el análisis de las variables.



## Productivización y Despliegue 
- Backend con **FastAPI**: endpoint `/predict` que recibe JSON y devuelve predicción.  
- Frontend en **React + Tailwind** con formulario intuitivo.  
- Base de datos **PostgresSQL**.

---

## Arquitectura del Sistema

```plaintext
Frontend (React + Tailwind)
        ↓
Backend (FastAPI + Pydantic)
        ↓
Modelo (Random Forest GridSearchCV .pkl)

``` 

---
## Instalación y Ejecución
🔧 Requisitos
- Python ≥ 3.10
- Node.js ≥ 18


---
## Pasos

Clonar el repositorio
```plaintext
git clone https://github.com/<usuario>/<repositorio>.git
cd <repositorio>
``` 
Acceder a la aplicación web
```plaintext
Frontend: cd client && npm run dev
Backend API Docs: http://localhost:8000/docs

Levantar el servidor 
Backend: uvicorn backend.main:app --reload
```


---
## Tecnologías Principales

| Componente      | Tecnología                                 |
| --------------- | ------------------------------------------ |
| Backend         | FastAPI, Pydantic, Alembic, PostgreSQL     |
| Frontend        | React, TailwindCSS, vite                   |
| Modelo ML       | Logistic Regression, KNN, Decision Tree    |
|                 | Random Forest, XGBoost, scikit-learn       |
| Colaboración    | GitHub, Git Projects  Conventional Commits |

---
## Variables más influyentes:
- Inflight Service
- Customer Type
- Online Boarding
- Checking Service
- Baggage Handling
- Seat Comfort
- Class
- Cleanliness
- OnBoard Service
- Inflight Wifi Service

---
# Entregables del proyecto: 
(Da click en cada nombre, te llevará al enlace correspondiente)

## 1. Aplicación: 


## 2. Informe Técnico
Puedes consultar el Informe Técnico completo con el detalle del análisis, desarrollo y resultados en el siguiente enlace:

- Descargar Informe Técnico (PDF): ![Informe técnico Passenger Satisfaction](docs/Informe_tecnico_passenger_satisfaction_PVI_Eq3.pdf)

## 3.  Presentación:
- ![Presentación comercial y técnica](https://www.canva.com/design/DAG1AK9ch5Q/rnldsVgfWjZABMhU52n23g/edit?utm_content=DAG1AK9ch5Q&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton)


## 4. Git Projects: 

 - ![Git Projects](https://drive.google.com/file/d/1oz7ngzBgK7acP5dITp0i9T_0NI33EHuO/view?usp=drive_link)

## 5. Otros: 
- ![Carpeta en la que organizamos entregables](https://drive.google.com/drive/folders/1-uul70XgQp3TDPcD-CMsN2Bbi8kcHG2_?usp=sharing)

Encontrarán: 

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
