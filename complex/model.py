# =======================================================================================
#                        IEXE Tec - Maestría en Ciencia de Datos
#                                  Productos de Datos
# ---------------------------------------------------------------------------------------
# En esta clase implementa la interacción con tu modelo.
# =======================================================================================
import random

# =======================================================================================
class Model:

    @classmethod
    def get_rating(cls, data):
        """ Aquí llama a tu modelo para recibir una predicción o una clase.
            :param cls: La clase que contiene el modelo. Puedes usarla para llamar a otros 
                        métodos de tu modelo.
            :param data: Los datos de la observación con la que vas a llamar al modelo
        """
        rate = random.uniform(0, 1)
        return '{:03.3f}'.format(rate)
