import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
import os

class SistemaLogin:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Sistema de Login - Gestión de Ventas")
        self.root.geometry("900x700")  
        self.root.resizable(True, True)  
        self.root.configure(bg='#f0f0f0')  
        
        self.center_window()
        self.cargar_datos()
        self.pantalla_actual = None
        self.mostrar_login()
        
    def center_window(self):
        """Centrar la ventana en la pantalla"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def cargar_datos(self):
        self.usuarios = {
            "admin": {"password": "admin123", "email": "admin@empresa.com", 
                     "pregunta": "¿Nombre de tu mascota?", "respuesta": "max"},
            "usuario1": {"password": "password1", "email": "usuario1@empresa.com",
                        "pregunta": "¿Ciudad de nacimiento?", "respuesta": "lima"},
            "vendedor": {"password": "ventas123", "email": "vendedor@empresa.com",
                        "pregunta": "¿Color favorito?", "respuesta": "azul"},
            "cliente": {"password": "cliente123", "email": "cliente@empresa.com",
                       "pregunta": "¿Mejor amigo?", "respuesta": "juan"}
        }
    
        self.productos = [
            {"id": 1, "nombre": "TornillosX500", "precio": 1850.00, "stock": 15, "categoria": "Herramienta"},
            {"id": 2, "nombre": "Destornillador Phillips", "precio": 35.50, "stock": 45, "categoria": "Herramienta"},
            {"id": 3, "nombre": "Tuvo PVC X 5M", "precio": 89.99, "stock": 20, "categoria": "Material"},
            {"id": 4, "nombre": "Lamparita LED", "precio": 299.99, "stock": 12, "categoria": "Repueesto"},
            {"id": 5, "nombre": "Caja Clavos", "precio": 249.99, "stock": 80, "categoria": "Herramienta"},
            {"id": 6, "nombre": "Taladro Electrico", "precio": 79.99, "stock": 30, "categoria": "Herramienta electrica"},
            {"id": 7, "nombre": "Repuesto Freno de Mano", "precio": 89.99, "stock": 25, "categoria": "Repuesto"},
            {"id": 8, "nombre": "Aceite WD40", "precio": 129.99, "stock": 18, "categoria": "Material"},
            {"id": 9, "nombre": "Repuesto Lampara Guiño", "precio": 59.99, "stock": 220, "categoria": "Repuesto"},
            {"id": 10, "nombre": "Llave inglesa", "precio": 399.99, "stock": 100, "categoria": "Herramienta"}
        ]
        
        self.carrito = []
        self.usuario_actual = None
        self.ventas_realizadas = []
    
    def limpiar_pantalla(self):
        if self.pantalla_actual:
            self.pantalla_actual.destroy()
    
    def mostrar_login(self):
        self.limpiar_pantalla()
        self.usuario_actual = None
        
        self.pantalla_actual = tk.Frame(self.root, bg='#f0f0f0', padx=30, pady=30)
        self.pantalla_actual.pack(fill=tk.BOTH, expand=True)
        
        frame_principal = tk.Frame(self.pantalla_actual, bg='white', relief=tk.RAISED, bd=2, padx=40, pady=40)
        frame_principal.pack(expand=True)
        
        tk.Label(frame_principal, text="🔐 Ferreteria ¡Que Tornillo!", 
                font=("Arial", 20, "bold"), bg='white', fg='#2c3e50').pack(pady=20)
        
        frame_form = tk.Frame(frame_principal, bg='white')
        frame_form.pack(pady=20)
        
        # Usuario
        tk.Label(frame_form, text="Usuario:", 
                font=("Arial", 12), bg='white').grid(row=0, column=0, sticky="w", pady=(10, 5))
        self.entry_usuario = tk.Entry(frame_form, font=("Arial", 12), width=25, bd=2, relief=tk.SUNKEN)
        self.entry_usuario.grid(row=0, column=1, pady=(10, 5), padx=(10, 0))
        
        # Contraseña
        tk.Label(frame_form, text="Contraseña:", 
                font=("Arial", 12), bg='white').grid(row=1, column=0, sticky="w", pady=5)
        self.entry_password = tk.Entry(frame_form, show="*", font=("Arial", 12), width=25, bd=2, relief=tk.SUNKEN)
        self.entry_password.grid(row=1, column=1, pady=5, padx=(10, 0))
        
        # Botones principales
        frame_botones_principales = tk.Frame(frame_principal, bg='white')
        frame_botones_principales.pack(pady=20)
        
        tk.Button(frame_botones_principales, text="🚀 Iniciar Sesión", bg="#27ae60", fg="white",
                 font=("Arial", 12, "bold"), command=self.iniciar_sesion,
                 width=15, height=2, bd=0, cursor="hand2").pack(side=tk.LEFT, padx=10)
        
        # Frame botones secundarios
        frame_botones_secundarios = tk.Frame(frame_principal, bg='white')
        frame_botones_secundarios.pack(pady=10)
        
        tk.Button(frame_botones_secundarios, text="🔍 Olvidé Usuario", bg="#3498db", fg="white",
                 font=("Arial", 10), command=self.recuperar_usuario,
                 width=15, bd=0, cursor="hand2").pack(side=tk.LEFT, padx=5)
        
        tk.Button(frame_botones_secundarios, text="🔑 Olvidé Contraseña", bg="#f39c12", fg="white",
                 font=("Arial", 10), command=self.recuperar_password,
                 width=15, bd=0, cursor="hand2").pack(side=tk.LEFT, padx=5)
        
        # Botón salir
        tk.Button(frame_principal, text="❌ Salir", bg="#e74c3c", fg="white",
                 font=("Arial", 10, "bold"), command=self.root.quit,
                 width=10, bd=0, cursor="hand2").pack(pady=20)
        
        # Información de usuarios demo
        frame_info = tk.Frame(frame_principal, bg='#ecf0f1', relief=tk.SUNKEN, bd=1)
        frame_info.pack(pady=10, fill=tk.X)
        
        info_text = "💡 Usuarios demo: admin/admin123 | usuario1/password1 | vendedor/ventas123"
        tk.Label(frame_info, text=info_text, font=("Arial", 8), bg='#ecf0f1', fg='#7f8c8d').pack(pady=5)
        
        # Focus en usuario
        self.entry_usuario.focus()
        
        # Bind Enter key
        self.entry_password.bind('<Return>', lambda event: self.iniciar_sesion())
    
    def iniciar_sesion(self):
        usuario = self.entry_usuario.get().strip()
        password = self.entry_password.get().strip()
        
        if not usuario or not password:
            messagebox.showerror("Error", "Por favor complete todos los campos")
            return
        
        if usuario in self.usuarios and self.usuarios[usuario]["password"] == password:
            self.usuario_actual = usuario
            messagebox.showinfo("Éxito", f"¡Bienvenido {usuario}!")
            self.mostrar_menu_principal()
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")
    
    def recuperar_usuario(self):
        email = simpledialog.askstring("Recuperar Usuario", 
                                      "Ingrese su email registrado:")
        if email:
            for usuario, datos in self.usuarios.items():
                if datos["email"] == email:
                    messagebox.showinfo("Usuario Recuperado", 
                                      f"Su usuario es: {usuario}")
                    return
            messagebox.showerror("Error", "Email no encontrado")
    
    def recuperar_password(self):
        usuario = simpledialog.askstring("Recuperar Contraseña", 
                                        "Ingrese su nombre de usuario:")
        if usuario and usuario in self.usuarios:
            pregunta = self.usuarios[usuario]["pregunta"]
            respuesta = simpledialog.askstring("Pregunta de Seguridad", 
                                             f"{pregunta}\n\nRespuesta:")
            if respuesta and respuesta.lower() == self.usuarios[usuario]["respuesta"]:
                messagebox.showinfo("Contraseña Recuperada", 
                                  f"Su contraseña es: {self.usuarios[usuario]['password']}")
            else:
                messagebox.showerror("Error", "Respuesta incorrecta")
        else:
            messagebox.showerror("Error", "Usuario no encontrado")
    
    def mostrar_menu_principal(self):
        self.limpiar_pantalla()
        
        self.pantalla_actual = tk.Frame(self.root, bg='#f0f0f0')
        self.pantalla_actual.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Título
        frame_titulo = tk.Frame(self.pantalla_actual, bg='#2c3e50')
        frame_titulo.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(frame_titulo, text=f"🎯 PANEL PRINCIPAL - {self.usuario_actual.upper()}", 
                font=("Arial", 18, "bold"), bg='#2c3e50', fg='white', pady=15).pack()
        
        # Frame de botones
        frame_botones = tk.Frame(self.pantalla_actual, bg='#f0f0f0')
        frame_botones.pack(expand=True)
        
        # Botones del menú con iconos y colores
        botones = [
            ("🛍️ VENTAS", self.mostrar_ventas, "#e74c3c"),
            ("🛒 CARRITO", self.mostrar_carrito, "#f39c12"),
            ("📦 PRODUCTOS", self.mostrar_productos, "#27ae60"),
            ("📊 REPORTES", self.mostrar_reportes, "#9b59b6"),
            ("👤 MI CUENTA", self.mostrar_cuenta, "#3498db"),
            ("🚪 CERRAR SESIÓN", self.cerrar_sesion, "#7f8c8d")
        ]
        
        # Crear botones en grid 2x3
        for i, (texto, comando, color) in enumerate(botones):
            row = i // 3
            col = i % 3
            btn = tk.Button(frame_botones, text=texto, font=("Arial", 12, "bold"),
                          bg=color, fg="white", command=comando, width=15, height=3,
                          bd=0, cursor="hand2")
            btn.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
        
        # Configurar grid para que se expanda
        for i in range(2):
            frame_botones.grid_rowconfigure(i, weight=1)
        for i in range(3):
            frame_botones.grid_columnconfigure(i, weight=1)
        
        # Footer
        frame_footer = tk.Frame(self.pantalla_actual, bg='#ecf0f1')
        frame_footer.pack(fill=tk.X, pady=(20, 0))
        
        tk.Label(frame_footer, text="Sistema de Gestión de Ventas v1.0", 
                font=("Arial", 8), bg='#ecf0f1', fg='#7f8c8d').pack(pady=5)
    
    def mostrar_ventas(self):
        self.limpiar_pantalla()
        
        self.pantalla_actual = tk.Frame(self.root, bg='#f0f0f0')
        self.pantalla_actual.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Título
        frame_titulo = tk.Frame(self.pantalla_actual, bg='#e74c3c')
        frame_titulo.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(frame_titulo, text="🛍️ VENTAS - CATÁLOGO DE PRODUCTOS", 
                font=("Arial", 16, "bold"), bg='#e74c3c', fg='white', pady=10).pack()
        
        # Frame principal
        frame_principal = tk.Frame(self.pantalla_actual, bg='#f0f0f0')
        frame_principal.pack(fill=tk.BOTH, expand=True)
        
        # Frame de búsqueda
        frame_busqueda = tk.Frame(frame_principal, bg='#f0f0f0')
        frame_busqueda.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(frame_busqueda, text="🔍 Buscar:", font=("Arial", 10), bg='#f0f0f0').pack(side=tk.LEFT, padx=(0, 5))
        
        self.entry_busqueda_ventas = tk.Entry(frame_busqueda, font=("Arial", 10), width=30)
        self.entry_busqueda_ventas.pack(side=tk.LEFT, padx=(0, 10))
        self.entry_busqueda_ventas.bind('<KeyRelease>', self.buscar_ventas)
        
        tk.Button(frame_busqueda, text="Limpiar", font=("Arial", 9), 
                 command=self.limpiar_busqueda_ventas).pack(side=tk.LEFT)
        
        # Treeview con scrollbar
        frame_tree = tk.Frame(frame_principal, bg='#f0f0f0')
        frame_tree.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        # Configurar treeview
        columns = ("ID", "Producto", "Categoría", "Precio", "Stock", "Estado")
        self.tree_ventas = ttk.Treeview(frame_tree, columns=columns, show="headings", height=15)
        
        # Configurar columnas
        column_widths = [50, 250, 120, 80, 60, 100]
        for col, width in zip(columns, column_widths):
            self.tree_ventas.heading(col, text=col)
            self.tree_ventas.column(col, width=width, anchor=tk.CENTER)
        
        self.tree_ventas.column("Producto", anchor=tk.W)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(frame_tree, orient=tk.VERTICAL, command=self.tree_ventas.yview)
        self.tree_ventas.configure(yscrollcommand=scrollbar.set)
        
        # Insertar datos
        self.actualizar_tree_ventas()
        
        self.tree_ventas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Frame de botones de acción
        frame_acciones = tk.Frame(frame_principal, bg='#f0f0f0')
        frame_acciones.pack(fill=tk.X, pady=(0, 10))
        
        tk.Button(frame_acciones, text="➕ Agregar al Carrito", bg="#27ae60", fg="white",
                 font=("Arial", 11, "bold"), command=lambda: self.agregar_al_carrito(self.tree_ventas),
                 width=20, bd=0, cursor="hand2").pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Button(frame_acciones, text="🛒 Ver Carrito", bg="#f39c12", fg="white",
                 font=("Arial", 11), command=self.mostrar_carrito,
                 width=15, bd=0, cursor="hand2").pack(side=tk.LEFT, padx=(0, 10))
        
        # Frame de botones de navegación
        frame_navegacion = tk.Frame(frame_principal, bg='#f0f0f0')
        frame_navegacion.pack(fill=tk.X)
        
        tk.Button(frame_navegacion, text="🔙 Volver al Menú", bg="#3498db", fg="white",
                 font=("Arial", 11), command=self.mostrar_menu_principal,
                 width=15, bd=0, cursor="hand2").pack(side=tk.LEFT)
        
        # Estadísticas rápidas
        total_productos = len(self.productos)
        total_stock = sum(p["stock"] for p in self.productos)
        productos_disponibles = sum(1 for p in self.productos if p["stock"] > 0)
        
        frame_stats = tk.Frame(frame_principal, bg='#ecf0f1', relief=tk.SUNKEN, bd=1)
        frame_stats.pack(fill=tk.X, pady=(10, 0))
        
        stats_text = f"📊 Estadísticas: {total_productos} productos | {total_stock} en stock | {productos_disponibles} disponibles"
        tk.Label(frame_stats, text=stats_text, font=("Arial", 9), bg='#ecf0f1', fg='#2c3e50').pack(pady=5)
    
    def buscar_ventas(self, event=None):
        """Función de búsqueda para la sección de ventas"""
        busqueda = self.entry_busqueda_ventas.get().lower().strip()
        
        # Limpiar treeview
        for item in self.tree_ventas.get_children():
            self.tree_ventas.delete(item)
        
        # Si no hay búsqueda, mostrar todos los productos
        if not busqueda:
            self.actualizar_tree_ventas()
            return
        
        # Filtrar productos según la búsqueda
        productos_filtrados = []
        for producto in self.productos:
            if (busqueda in str(producto["id"]).lower() or 
                busqueda in producto["nombre"].lower() or 
                busqueda in producto["categoria"].lower() or
                busqueda in str(producto["precio"]).lower()):
                productos_filtrados.append(producto)
        
        # Insertar productos filtrados
        for producto in productos_filtrados:
            estado = "✅ Disponible" if producto["stock"] > 0 else "❌ Agotado"
            self.tree_ventas.insert("", tk.END, values=(
                producto["id"], 
                producto["nombre"], 
                producto["categoria"],
                f"${producto['precio']:.2f}", 
                producto["stock"],
                estado
            ))
    
    def limpiar_busqueda_ventas(self):
        """Limpiar la búsqueda en ventas"""
        self.entry_busqueda_ventas.delete(0, tk.END)
        self.actualizar_tree_ventas()
    
    def actualizar_tree_ventas(self):
        """Actualizar el treeview de ventas con todos los productos"""
        # Limpiar treeview
        for item in self.tree_ventas.get_children():
            self.tree_ventas.delete(item)
        
        # Insertar todos los productos
        for producto in self.productos:
            estado = "✅ Disponible" if producto["stock"] > 0 else "❌ Agotado"
            self.tree_ventas.insert("", tk.END, values=(
                producto["id"], 
                producto["nombre"], 
                producto["categoria"],
                f"${producto['precio']:.2f}", 
                producto["stock"],
                estado
            ))
    
    def agregar_al_carrito(self, tree):
        seleccion = tree.selection()
        if not seleccion:
            messagebox.showerror("Error", "Seleccione un producto primero")
            return
        
        item = tree.item(seleccion[0])
        producto_id = item["values"][0]
        producto_nombre = item["values"][1]
        producto_precio = float(item["values"][3].replace("$", ""))
        producto_stock = item["values"][4]
        
        if producto_stock <= 0:
            messagebox.showerror("Error", "Producto agotado")
            return
        
        # Ventana para cantidad
        cantidad = simpledialog.askinteger("Cantidad", 
                                         f"Cantidad de '{producto_nombre}'\n\nStock disponible: {producto_stock}",
                                         minvalue=1, maxvalue=producto_stock,
                                         parent=self.root)
        
        if cantidad:
            # Verificar si ya está en el carrito
            for item in self.carrito:
                if item["id"] == producto_id:
                    item["cantidad"] += cantidad
                    break
            else:
                self.carrito.append({
                    "id": producto_id,
                    "nombre": producto_nombre,
                    "precio": producto_precio,
                    "cantidad": cantidad
                })
            
            # Actualizar stock
            for producto in self.productos:
                if producto["id"] == producto_id:
                    producto["stock"] -= cantidad
                    break
            
            messagebox.showinfo("Éxito", f"✅ {cantidad} x {producto_nombre}\nAgregado al carrito!")
            
            # Actualizar vista
            self.mostrar_ventas()
    
    def mostrar_carrito(self):
        if not self.carrito:
            messagebox.showinfo("Carrito", "🛒 Tu carrito está vacío")
            return
        
        self.limpiar_pantalla()
        
        self.pantalla_actual = tk.Frame(self.root, bg='#f0f0f0')
        self.pantalla_actual.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Título
        frame_titulo = tk.Frame(self.pantalla_actual, bg='#f39c12')
        frame_titulo.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(frame_titulo, text="🛒 CARRITO DE COMPRAS", 
                font=("Arial", 16, "bold"), bg='#f39c12', fg='white', pady=10).pack()
        
        # Frame principal
        frame_principal = tk.Frame(self.pantalla_actual, bg='#f0f0f0')
        frame_principal.pack(fill=tk.BOTH, expand=True)
        
        # Treeview
        frame_tree = tk.Frame(frame_principal, bg='#f0f0f0')
        frame_tree.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        columns = ("Producto", "Cantidad", "Precio Unit.", "Subtotal")
        tree = ttk.Treeview(frame_tree, columns=columns, show="headings", height=12)
        
        column_widths = [300, 80, 100, 120]
        for col, width in zip(columns, column_widths):
            tree.heading(col, text=col)
            tree.column(col, width=width, anchor=tk.CENTER)
        
        tree.column("Producto", anchor=tk.W)
        
        scrollbar = ttk.Scrollbar(frame_tree, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        # Calcular totales
        total = 0
        for item in self.carrito:
            subtotal = item["precio"] * item["cantidad"]
            total += subtotal
            tree.insert("", tk.END, values=(
                item["nombre"],
                item["cantidad"],
                f"${item['precio']:.2f}",
                f"${subtotal:.2f}"
            ))
        
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Total
        frame_total = tk.Frame(frame_principal, bg='#2ecc71', relief=tk.RAISED, bd=2)
        frame_total.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(frame_total, text=f"💰 TOTAL A PAGAR: ${total:.2f}", 
                font=("Arial", 14, "bold"), bg='#2ecc71', fg='white', pady=10).pack()
        
        # Frame de botones de acción
        frame_acciones = tk.Frame(frame_principal, bg='#f0f0f0')
        frame_acciones.pack(fill=tk.X, pady=(0, 10))
        
        tk.Button(frame_acciones, text="✅ Realizar Compra", bg="#27ae60", fg="white",
                 font=("Arial", 11, "bold"), command=self.realizar_compra,
                 width=15, bd=0, cursor="hand2").pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Button(frame_acciones, text="🗑️ Vaciar Carrito", bg="#e74c3c", fg="white",
                 font=("Arial", 11), command=self.vaciar_carrito,
                 width=15, bd=0, cursor="hand2").pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Button(frame_acciones, text="🛍️ Seguir Comprando", bg="#3498db", fg="white",
                 font=("Arial", 11), command=self.mostrar_ventas,
                 width=18, bd=0, cursor="hand2").pack(side=tk.LEFT)
        
        # Frame de botones de navegación
        frame_navegacion = tk.Frame(frame_principal, bg='#f0f0f0')
        frame_navegacion.pack(fill=tk.X)
        
        tk.Button(frame_navegacion, text="🔙 Volver al Menú", bg="#7f8c8d", fg="white",
                 font=("Arial", 11), command=self.mostrar_menu_principal,
                 width=15, bd=0, cursor="hand2").pack(side=tk.LEFT)
    
    def realizar_compra(self):
        if not self.carrito:
            return
        
        total = sum(item["precio"] * item["cantidad"] for item in self.carrito)
        
        # Registrar venta
        venta = {
            "id": len(self.ventas_realizadas) + 1,
            "usuario": self.usuario_actual,
            "fecha": "2024-01-01",  # Aquí podrías usar datetime.now()
            "total": total,
            "items": self.carrito.copy()
        }
        self.ventas_realizadas.append(venta)
        
        messagebox.showinfo("Compra Exitosa", 
                          f"🎉 ¡Compra realizada con éxito!\n\n"
                          f"📦 Productos: {sum(item['cantidad'] for item in self.carrito)}\n"
                          f"💰 Total: ${total:.2f}\n\n"
                          f"¡Gracias por su compra!")
        
        self.carrito.clear()
        self.mostrar_menu_principal()
    
    def vaciar_carrito(self):
        if not self.carrito:
            return
        
        if messagebox.askyesno("Confirmar", "¿Está seguro de vaciar el carrito?"):
            # Devolver productos al stock
            for item in self.carrito:
                for producto in self.productos:
                    if producto["id"] == item["id"]:
                        producto["stock"] += item["cantidad"]
                        break
            
            self.carrito.clear()
            messagebox.showinfo("Carrito", "🗑️ Carrito vaciado")
            self.mostrar_ventas()
    
    def mostrar_productos(self):
        self.limpiar_pantalla()
        
        self.pantalla_actual = tk.Frame(self.root, bg='#f0f0f0')
        self.pantalla_actual.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Título
        frame_titulo = tk.Frame(self.pantalla_actual, bg='#27ae60')
        frame_titulo.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(frame_titulo, text="📦 INVENTARIO DE PRODUCTOS", 
                font=("Arial", 16, "bold"), bg='#27ae60', fg='white', pady=10).pack()
        
        # Frame principal
        frame_principal = tk.Frame(self.pantalla_actual, bg='#f0f0f0')
        frame_principal.pack(fill=tk.BOTH, expand=True)
        
        # Frame de búsqueda
        frame_busqueda = tk.Frame(frame_principal, bg='#f0f0f0')
        frame_busqueda.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(frame_busqueda, text="🔍 Buscar:", font=("Arial", 10), bg='#f0f0f0').pack(side=tk.LEFT, padx=(0, 5))
        
        self.entry_busqueda_productos = tk.Entry(frame_busqueda, font=("Arial", 10), width=30)
        self.entry_busqueda_productos.pack(side=tk.LEFT, padx=(0, 10))
        self.entry_busqueda_productos.bind('<KeyRelease>', self.buscar_productos)
        
        tk.Button(frame_busqueda, text="Limpiar", font=("Arial", 9), 
                 command=self.limpiar_busqueda_productos).pack(side=tk.LEFT)
        
        # Treeview con scrollbar
        frame_tree = tk.Frame(frame_principal, bg='#f0f0f0')
        frame_tree.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        # Configurar treeview
        columns = ("ID", "Producto", "Categoría", "Precio", "Stock", "Estado")
        self.tree_productos = ttk.Treeview(frame_tree, columns=columns, show="headings", height=15)
        
        # Configurar columnas
        column_widths = [50, 250, 120, 80, 60, 100]
        for col, width in zip(columns, column_widths):
            self.tree_productos.heading(col, text=col)
            self.tree_productos.column(col, width=width, anchor=tk.CENTER)
        
        self.tree_productos.column("Producto", anchor=tk.W)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(frame_tree, orient=tk.VERTICAL, command=self.tree_productos.yview)
        self.tree_productos.configure(yscrollcommand=scrollbar.set)
        
        # Insertar datos
        self.actualizar_tree_productos()
        
        self.tree_productos.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Frame de botones de navegación
        frame_botones = tk.Frame(frame_principal, bg='#f0f0f0')
        frame_botones.pack(fill=tk.X, pady=20)
        
        tk.Button(frame_botones, text="🔙 Volver al Menú", bg="#3498db", fg="white",
                 font=("Arial", 11), command=self.mostrar_menu_principal,
                 width=15, bd=0, cursor="hand2").pack(side=tk.LEFT)
    
    def buscar_productos(self, event=None):
        """Función de búsqueda para la sección de productos"""
        busqueda = self.entry_busqueda_productos.get().lower().strip()
        
        # Limpiar treeview
        for item in self.tree_productos.get_children():
            self.tree_productos.delete(item)
        
        # Si no hay búsqueda, mostrar todos los productos
        if not busqueda:
            self.actualizar_tree_productos()
            return
        
        # Filtrar productos según la búsqueda
        productos_filtrados = []
        for producto in self.productos:
            if (busqueda in str(producto["id"]).lower() or 
                busqueda in producto["nombre"].lower() or 
                busqueda in producto["categoria"].lower() or
                busqueda in str(producto["precio"]).lower()):
                productos_filtrados.append(producto)
        
        # Insertar productos filtrados
        for producto in productos_filtrados:
            estado = "✅ Disponible" if producto["stock"] > 0 else "❌ Agotado"
            self.tree_productos.insert("", tk.END, values=(
                producto["id"], 
                producto["nombre"], 
                producto["categoria"],
                f"${producto['precio']:.2f}", 
                producto["stock"],
                estado
            ))
    
    def limpiar_busqueda_productos(self):
        """Limpiar la búsqueda en productos"""
        self.entry_busqueda_productos.delete(0, tk.END)
        self.actualizar_tree_productos()
    
    def actualizar_tree_productos(self):
        """Actualizar el treeview de productos con todos los productos"""
        # Limpiar treeview
        for item in self.tree_productos.get_children():
            self.tree_productos.delete(item)
        
        # Insertar todos los productos
        for producto in self.productos:
            estado = "✅ Disponible" if producto["stock"] > 0 else "❌ Agotado"
            self.tree_productos.insert("", tk.END, values=(
                producto["id"], 
                producto["nombre"], 
                producto["categoria"],
                f"${producto['precio']:.2f}", 
                producto["stock"],
                estado
            ))
    
    def mostrar_reportes(self):
        self.limpiar_pantalla()
        
        self.pantalla_actual = tk.Frame(self.root, bg='#f0f0f0')
        self.pantalla_actual.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Título
        tk.Label(self.pantalla_actual, text="📊 REPORTES Y ESTADÍSTICAS", 
                font=("Arial", 16, "bold"), bg='#f0f0f0', fg='#2c3e50').pack(pady=10)
        
        # Frame de estadísticas
        frame_stats = tk.Frame(self.pantalla_actual, bg='white', relief=tk.RAISED, bd=2, padx=20, pady=20)
        frame_stats.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Estadísticas
        total_ventas = len(self.ventas_realizadas)
        total_productos = len(self.productos)
        total_carrito = len(self.carrito)
        total_ingresos = sum(venta["total"] for venta in self.ventas_realizadas)
        
        stats = [
            f"📈 Ventas realizadas: {total_ventas}",
            f"💰 Ingresos totales: ${total_ingresos:.2f}",
            f"📦 Productos en sistema: {total_productos}",
            f"🛒 Items en carrito: {total_carrito}",
            f"👤 Usuario actual: {self.usuario_actual}"
        ]
        
        for stat in stats:
            tk.Label(frame_stats, text=stat, font=("Arial", 12), bg='white', 
                    justify=tk.LEFT).pack(anchor="w", pady=5)
        
        # Botones
        frame_botones = tk.Frame(self.pantalla_actual, bg='#f0f0f0')
        frame_botones.pack(fill=tk.X, pady=20)
        
        tk.Button(frame_botones, text="🔄 Actualizar", bg="#3498db", fg="white",
                 font=("Arial", 11), command=self.mostrar_reportes,
                 width=12, bd=0, cursor="hand2").pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Button(frame_botones, text="🔙 Volver al Menú", bg="#7f8c8d", fg="white",
                 font=("Arial", 11), command=self.mostrar_menu_principal,
                 width=15, bd=0, cursor="hand2").pack(side=tk.LEFT)
    
    def mostrar_cuenta(self):
        messagebox.showinfo("Mi Cuenta", 
                          f"👤 Información de cuenta:\n\n"
                          f"Usuario: {self.usuario_actual}\n"
                          f"Email: {self.usuarios[self.usuario_actual]['email']}\n"
                          f"Pregunta de seguridad: {self.usuarios[self.usuario_actual]['pregunta']}")
    
    def cerrar_sesion(self):
        if messagebox.askyesno("Cerrar Sesión", "¿Está seguro de cerrar la sesión?"):
            self.usuario_actual = None
            self.carrito.clear()
            self.mostrar_login()
    
    def ejecutar(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = SistemaLogin()
    app.ejecutar()