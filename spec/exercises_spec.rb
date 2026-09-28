# spec/exercises_spec.rb
require 'open3'

RSpec.describe "ANEPSA TI - Validación de Scripts (Caso 8)" do
  context "Ejercicio A: Healthcheck Script" do
    it "existe el script healthcheck.py en la ruta esperada" do
      expect(File.exist?("healthcheck.py")).to be(true)
    end

    it "ejecuta el modo de prueba de healthcheck.py sin errores" do
      stdout, stderr, status = Open3.capture3("python3 healthcheck.py --test")
      expect(status.success?).to be(true)
      expect(stdout).to include("MODO DE PRUEBA Y SIMULACIÓN")
    end
  end

  context "Ejercicio B: Sprint Report Script" do
    it "existe el script sprint_report.py en la ruta esperada" do
      expect(File.exist?("sprint_report.py")).to be(true)
    end

    it "genera o lee correctamente sprint_data.json y emite el reporte ejecutivo" do
      stdout, stderr, status = Open3.capture3("python3 sprint_report.py")
      expect(status.success?).to be(true)
      expect(stdout).to include("REPORTE EJECUTIVO DE ESTADO DE SPRINT")
    end
  end
end