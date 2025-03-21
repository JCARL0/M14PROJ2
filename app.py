from flask import Flask, render_template, request
import pandas as pd

# Crear la aplicacion Flask
app = Flask(__name__)

# Leer archivo CSV y crear DataFrame
df = pd.read_csv("Alumnes_matriculats_per_ensenyament_i_unitats_dels_centres_docents_20250320.csv", sep=",", on_bad_lines='skip')

# Seleccionar columnas necesarias y eliminar filas con valores nulos
df = df[['Curs', 'Denominació completa', 'Nom naturalesa', 'Nom àrea territorial', 
         'Grau', 'Nom ensenyament', 'Modalitat', 'Matrícules. Dones', 'Matrícules. Homes']]
df = df.dropna()

# Preparar los filtros con pandas, ordenando los valores unicos
filtros = {
    "cursos": df["Curs"].dropna().sort_values().unique(),
    "centros": df["Denominació completa"].dropna().sort_values().unique(),
    "naturalezas": df["Nom naturalesa"].dropna().sort_values().unique(),
    "areas": df["Nom àrea territorial"].dropna().sort_values().unique(),
    "grados": df["Grau"].dropna().sort_values().unique(),
    "enseñanzas": df["Nom ensenyament"].dropna().sort_values().unique(),
    "modalidades": df["Modalitat"].dropna().sort_values().unique(),
}

# Ruta principal de la aplicacion
@app.route("/", methods=["GET", "POST"])
def index():
    resultados = None

    # Si se envia el formulario
    if request.method == "POST":
        # Obtener datos del formulario
        curso = request.form["curso"]
        centro = request.form["centro"]
        naturaleza = request.form["naturaleza"]
        area = request.form["area"]
        grado = request.form["grado"]
        enseñanza = request.form["enseñanza"]
        modalidad = request.form["modalidad"]

        # Filtrar el DataFrame segun los valores seleccionados
        df_filtrado = df
        if curso:
            df_filtrado = df_filtrado.loc[df_filtrado["Curs"] == curso]
        if centro:
            df_filtrado = df_filtrado.loc[df_filtrado["Denominació completa"] == centro]
        if naturaleza:
            df_filtrado = df_filtrado.loc[df_filtrado["Nom naturalesa"] == naturaleza]
        if area:
            df_filtrado = df_filtrado.loc[df_filtrado["Nom àrea territorial"] == area]
        if grado:
            df_filtrado = df_filtrado.loc[df_filtrado["Grau"] == grado]
        if enseñanza:
            df_filtrado = df_filtrado.loc[df_filtrado["Nom ensenyament"] == enseñanza]
        if modalidad:
            df_filtrado = df_filtrado.loc[df_filtrado["Modalitat"] == modalidad]

        # Calcular suma de matriculas de mujeres y hombres
        total_mujeres = df_filtrado["Matrícules. Dones"].sum()
        total_hombres = df_filtrado["Matrícules. Homes"].sum()
        total = total_mujeres + total_hombres

        # Guardar resultados
        resultados = {
            "mujeres": total_mujeres,
            "hombres": total_hombres,
            "total": total
        }

    # Mostrar pagina con filtros y resultados
    return render_template("index.html", filtros=filtros, resultados=resultados)

# Ejecutar aplicacion
if __name__ == "__main__":
    app.run()
