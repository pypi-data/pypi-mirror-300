# gestor_ventas/precios.py
#@staticmethod es un decorador en Python que se utiliza para definir un método estático dentro de una clase. Los métodos estáticos son aquellos que no dependen de una instancia particular de la clase y no tienen acceso a los atributos o métodos de la instancia (es decir, no pueden acceder a self). 
class Precios:
    @staticmethod
    def calcular_precio_final(precio_base, impuesto, descuento):
        return precio_base + impuesto - descuento
