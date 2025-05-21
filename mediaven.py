class MedicalAIAgent:
    def __init__(self):
        # Base de conocimiento médica (simulada)
        self.sintomas_enfermedades = {
            "gripe": {"fiebre", "tos", "dolor de cabeza", "fatiga"},
            "neumonia": {"fiebre", "tos con flema", "dolor torácico", "disnea"},
            "anemia": {"fatiga", "palidez", "mareos", "falta de aire"},
            "diabetes": {"sed excesiva", "micción frecuente", "hambre constante", "vision borrosa"},
            "alergia": {"rash cutaneo", "picazón", "dificultad respiratoria", "swelling"},
            "migraña": {"dolor de cabeza intenso", "náuseas", "fotofobia", "sonolencia"},
            "gastroenteritis": {"vómitos", "diarrea", "fiebre baja", "dolor abdominal"}
        }
        
        # Mapeo de tratamientos
        self.tratamientos = {
            "gripe": ["Descanso", "Hidratación", "Paracetamol"],
            "neumonia": ["Antibióticos", "Oxígeno", "Control de fiebre"],
            "anemia": ["Hierro oral", "Dieta rica en hierro", "Evitar esfuerzos"],
            "diabetes": ["Insulina", "Control glucémico", "Dieta balanceada"],
            "alergia": ["Antihistamínicos", "Evitar alérgenos", "Hidratación"],
            "migraña": ["Sumatriptán", "Evitar estimulantes", "Ambiente tranquilo"],
            "gastroenteritis": ["Rehidratación", "Antidiarréicos", "Dieta blanda"]
        }

    def _calcular_confianza(self, sintomas_usuario, enfermedad):
        """Calcula la confianza basada en coincidencias de síntomas"""
        coincidencias = len(sintomas_usuario & self.sintomas_enfermedades[enfermedad])
        return coincidencias / len(self.sintomas_enfermedades[enfermedad])

    def diagnosticar(self, sintomas_usuario):
        """Genera un diagnóstico basado en síntomas"""
        resultados = {}
        for enfermedad in self.sintomas_enfermedades:
            confianza = self._calcular_confianza(sintomas_usuario, enfermedad)
            if confianza > 0.3:  # Umbral mínimo de confianza
                resultados[enfermedad] = confianza
        
        # Selecciona la enfermedad con mayor confianza
        if resultados:
            diagnostico = max(resultados, key=resultados.get)
            return {
                "enfermedad": diagnostico,
                "confianza": round(resultados[diagnostico], 2),
                "sintomas_coincididos": list(sintomas_usuario & self.sintomas_enfermedades[diagnostico])
            }
        else:
            return None

    def sugerir_tratamiento(self, diagnostico):
        """Proporciona recomendaciones médicas"""
        return self.tratamientos.get(diagnostico, ["Consultar a un médico"])
    

# Ejemplo de uso
if __name__ == "__main__":
    agente = MedicalAIAgent()
    
    print("Ingrese sus síntomas uno por uno. Escriba 'listo' cuando termine.")
    sintomas = []
    while True:
        entrada = input("Síntoma: ").strip().lower()
        if entrada == "listo":
            break
        # Limpiar y formatear el síntoma (ej.: "dolor de cabeza" → "dolor_de_cabeza")
        sintoma_formateado = entrada.replace(" ", "_")
        sintomas.append(sintoma_formateado)
    
    
    # Generar diagnóstico
    diagnostico = agente.diagnosticar(set(sintomas))
    if diagnostico:
        print("\nResultado del diagnóstico:")
        print(f"Enfermedad más probable: {diagnostico['enfermedad']}")
        print(f"Confianza: {diagnostico['confianza'] * 100:.1f}%")
        print("Síntomas que coincidieron:", ", ".join(diagnostico['sintomas_coincididos']))
        
        # Recomendaciones
        print("\nRecomendaciones médicas:")
        for i, tratamiento in enumerate(agente.sugerir_tratamiento(diagnostico['enfermedad']), 1):
            print(f"{i}. {tratamiento}")
    else:
        print("No se encontró un diagnóstico coincidente. Consulte a un profesional.")