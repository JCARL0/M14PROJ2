from flask import Flask, render_template, request
import pandas as pd

# Crear la aplicacion de Flask
app = Flask(__name__)

# Cargar el archivo CSV con los datos
CSV_FILE = "Alumnes_matriculats_per_ensenyament_i_unitats_dels_centres_docents_20250320.csv"
df = pd.read_csv(CSV_FILE, sep=",", on_bad_lines='skip')

# Limpiar los datos eliminando columnas innecesarias y gestionando los valores nulos
df = df[['Curs', 'Denominació completa', 'Nom naturalesa', 'Nom àrea territorial', 
         'Grau', 'Nom ensenyament', 'Modalitat', 'Matrícules. Dones', 'Matrícules. Homes']].dropna()

# Obtener los valores unicos de las columnas para usarlos en los filtros
filtros = {
    "cursos": sorted(df["Curs"].unique()), 
    "centros": sorted(df["Denominació completa"].unique()),
    "naturalezas": sorted(df["Nom naturalesa"].unique()),
    "areas": sorted(df["Nom àrea territorial"].unique()),
    "grados": sorted(df["Grau"].dropna().unique()),
    "enseñanzas": sorted(df["Nom ensenyament"].unique()),
    "modalidades": sorted(df["Modalitat"].dropna().unique()),
}

# Ruta principal que maneja las peticiones GET y POST
@app.route("/", methods=["GET", "POST"])
def index():
    resultados = None
    # Si la peticion es POST (cuando el formulario se envia)
    if request.method == "POST":
        # Obtener los valores seleccionados en el formulario
        curso = request.form.get("curso")
        centro = request.form.get("centro")
        naturaleza = request.form.get("naturaleza")
        area = request.form.get("area")
        grado = request.form.get("grado")
        enseñanza = request.form.get("enseñanza")
        modalidad = request.form.get("modalidad")

        # Filtrar el dataframe con los valores seleccionados
        df_filter = df.copy()
        if curso: 
            df_filter = df_filter[df_filter["Curs"] == curso]
        if centro: 
            df_filter = df_filter[df_filter["Denominació completa"] == centro]
        if naturaleza: 
            df_filter = df_filter[df_filter["Nom naturalesa"] == naturaleza]
        if area: 
            df_filter = df_filter[df_filter["Nom àrea territorial"] == area]
        if grado: 
            df_filter = df_filter[df_filter["Grau"] == grado]
        if enseñanza: 
            df_filter = df_filter[df_filter["Nom ensenyament"] == enseñanza]
        if modalidad: 
            df_filter = df_filter[df_filter["Modalitat"] == modalidad]

        # Sumar el total de matriculas por genero
        total_mujeres = df_filter["Matrícules. Dones"].sum()
        total_hombres = df_filter["Matrícules. Homes"].sum()
        total_general = total_mujeres + total_hombres

        # Guardar los resultados para mostrarlos en la vista
        resultados = {
                "mujeres": total_mujeres,
                "hombres": total_hombres,
                "total": total_general
        }

    # Renderizar la plantilla con los filtros y resultados
    return render_template("index.html", filtros=filtros, resultados=resultados)

# Ejecutar la aplicacion
if __name__ == "__main__":
    app.run(host="localhost", port=5000, debug=False)
