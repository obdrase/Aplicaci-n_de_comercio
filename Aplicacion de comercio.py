class Producto:
    def __init__(self, sku, nombre, descripcion, unidades_disponibles, precio_unitario):
        self.sku = sku
        self.nombre = nombre
        self.descripcion = descripcion
        self.unidades_disponibles = unidades_disponibles
        self.precio_unitario = precio_unitario

    def tiene_unidades(self, cantidad):
        return self.unidades_disponibles >= cantidad

    def obtener_sku(self):
        return self.sku

    def descontar_unidades(self, cantidad):
        if self.tiene_unidades(cantidad):
            self.unidades_disponibles -= cantidad
            return True
        return False

class Item:
  def __init__(self, producto, cantidad):
        self.producto = producto
        self.cantidad = cantidad

  def calcular_total(self):
        return manejador.verificar_regla(self.producto, self.cantidad)

class Carrito:
    def __init__(self):
        self.items = []

    def agregar_item(self, producto, cantidad):
        if producto.tiene_unidades(cantidad):
            self.items.append(Item(producto, cantidad))
            producto.descontar_unidades(cantidad)

    def menu_eliminar_item(self):
        for i, item in enumerate(usuario.carrito.items):
            print(f"{i+1}.{item.producto.nombre} - Cantidad: {item.cantidad} - Total: ${manejador.verificar_regla(item.producto,item.cantidad)}")
        print(f"{len(usuario.carrito.items)+1}.Cancelar")
        try:
          opcion = int(input("Seleccione el item a eliminar: "))
          print(opcion)
          if opcion == len(usuario.carrito.items)+1:
              print("Operación cancelada.")
              return
          elif opcion > len(usuario.carrito.items):
              print("opcion inválida.")
          else:
            item_a_eliminar = usuario.carrito.items[opcion-1]
            self.borrar_item(item_a_eliminar)
        except ValueError:
            print("Entrada inválida.")
            return

    def borrar_item(self, item):
      item.producto.unidades_disponibles += item.cantidad
      self.items.remove(item)
      print("Item eliminado del carrito.")

    def calcular_total(self):
        return sum(item.calcular_total() for item in self.items)

    def menu_carrito(self):
      while True:
        print("Que desea hacer?")
        print("1. Volver al menu anterior")
        print("2. Eliminar producto")
        print("3. Finalizar compra")
        opcion = input("Seleccione una opción: ")
        if opcion == "1":
            return
        if opcion == "2":
            self.menu_eliminar_item()
            return
        if opcion == "3":
            tienda.finalizar_compra(usuario)
            return
        else:
            print("Opción inválida, intente de nuevo.")


class Usuario:
    def __init__(self):
        self.carrito = Carrito()

    def agregar_item_a_carrito(self, producto, cantidad):
        self.carrito.agregar_item(producto, cantidad)

    def borrar_item_de_carrito(self, item):
        self.carrito.borrar_item(item)

    def mostrar_carrito(self):
        print("Productos en tu carrito:")
        for item in usuario.carrito.items:
            print(f"{item.producto.nombre} - Cantidad: {item.cantidad} - Total: ${manejador.verificar_regla(item.producto,item.cantidad)}")
        print(f"Total a pagar: ${self.carrito.calcular_total()}")
        self.carrito.menu_carrito()

class Tienda:
    def __init__(self):
        self.total_ventas = 0.0
        self.usuarios = []
        self.productos = []

    def agregar_producto_a_carrito(self, usuario, producto, cantidad):
        usuario.agregar_item_a_carrito(producto, cantidad)

    def eliminar_item_de_carrito(self, usuario, item):
        usuario.borrar_item_de_carrito(item)

    def finalizar_compra(self, usuario):
        total = usuario.carrito.calcular_total()
        self.total_ventas += total
        usuario.carrito = Carrito()

    def mostrar_productos(self):
        print("Productos disponibles:")
        for i, producto in enumerate(self.productos):
            print(f"{i + 1}. {producto.nombre} - ${producto.precio_unitario} ({producto.unidades_disponibles} disponibles)")

    def agregar_producto(self):
        tienda.mostrar_productos()
        indice = self.obtener_indice_producto()
        if indice is None:
            return
        cantidad = self.obtener_cantidad_producto(tienda.productos[indice])
        if cantidad is None:
            return
        tienda.agregar_producto_a_carrito(usuario, tienda.productos[indice], cantidad)
        print("Producto agregado al carrito.")

    def obtener_indice_producto(self):
        try:
            indice = int(input("Seleccione el número del producto: ")) - 1
            if 0 <= indice < len(tienda.productos):
                return indice
            print("Selección inválida.")
        except ValueError:
            print("Entrada inválida.")
        return None

    def obtener_cantidad_producto(self, producto):
        try:
            if(producto.obtener_sku()=="WE"):
                cantidad = float(input("Ingrese la cantidad: "))
            else:
              cantidad = int(input("Ingrese la cantidad: "))
            if cantidad <= 0:
                print("La cantidad debe ser mayor que cero.")
            elif cantidad > producto.unidades_disponibles:
                print("No hay suficientes unidades disponibles.")
            else:
                return cantidad
        except ValueError:
            print("Entrada inválida.")
        return None

    def finalizar(self):
      self.finalizar_compra(usuario)

class manejador_de_reglas:
    def __init__(self):
        self.reglas = [regla_precio_normal(), regla_precio_por_peso(), regla_precio_especial()]

    def verificar_regla(self, Producto, cantidad):
        for regla in self.reglas:
            if regla.es_aplicable(Producto):
                return regla.calcular_precio(Producto, cantidad)
        print("No se encontró la regla.")
        return None


class regla_precio_normal:
    def es_aplicable(self, producto):
        return producto.obtener_sku() == "EA"

    def calcular_precio(self, producto, cantidad):
        return producto.precio_unitario * cantidad


class regla_precio_por_peso:
    def es_aplicable(self, producto):
        return producto.obtener_sku() == "WE"

    def calcular_precio(self, producto, cantidad):
        return producto.precio_unitario * cantidad


class regla_precio_especial:
    def es_aplicable(self, producto):
        return producto.obtener_sku() == "SP"

    def calcular_precio(self, producto, cantidad):
        if cantidad >= 9:
            return producto.precio_unitario * cantidad * 0.5
        if cantidad >= 6:
            return producto.precio_unitario * cantidad * 0.6
        if cantidad >= 3:
            return producto.precio_unitario * cantidad * 0.8
        else:
            return producto.precio_unitario * cantidad

# Menú de usuario
if __name__ == "__main__":
    tienda = Tienda()
    usuario = Usuario()
    manejador = manejador_de_reglas()

    tienda.productos.append(Producto("EA", "Laptop", "Laptop Gamer", 10, 1200.0))
    tienda.productos.append(Producto("EA", "Mouse", "Mouse Inalámbrico", 15, 50.0))
    tienda.productos.append(Producto("EA", "Teclado", "Teclado Mecánico", 8, 100.0))
    tienda.productos.append(Producto("WE", "Frijol", "Frijol por Kilo", 20, 2.0))
    tienda.productos.append(Producto("SP", "Memoria USB", "Memoria USB 4gb", 50, 20.0))

    switch = {
            "1": tienda.mostrar_productos,
            "2": tienda.agregar_producto,
            "3": usuario.mostrar_carrito,
            "4": tienda.finalizar,
        }

    while True:
        print("=============================================")
        print("\nMenú de la Tienda:")
        print("1. Ver productos")
        print("2. Agregar producto al carrito")
        print("3. Ver carrito")
        print("4. Finalizar compra")
        print("5. Salir")

        opcion = input("Seleccione una opción: ")


        if opcion == "5":
            print("Gracias por su visita!")
            break
        switch.get(opcion, lambda: print("Opción inválida"))()

