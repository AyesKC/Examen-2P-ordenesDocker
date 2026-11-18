CREATE DATABASE OrdenesDB;
GO

USE OrdenesDB;
GO

CREATE TABLE ordenes(
    id INT IDENTITY(1,1) PRIMARY KEY,
    cliente VARCHAR(100) NOT NULL,
    fecha DATETIME DEFAULT GETDATE(),
    estado VARCHAR(20) NOT NULL,
    total DECIMAL(10,2) DEFAULT 0
);
GO

CREATE TABLE orden_detalle(
    id INT IDENTITY(1,1) PRIMARY KEY,
    orden_id INT NOT NULL,
    producto VARCHAR(100) NOT NULL,
    cantidad INT NOT NULL,
    precio_unitario DECIMAL(10,2) NOT NULL,
    subtotal DECIMAL(10,2) NOT NULL,

    FOREIGN KEY (orden_id)
    REFERENCES ordenes(id)
);
GO

INSERT INTO ordenes(cliente,estado,total)
VALUES
('Juan Perez','Pendiente',500),
('Maria Lopez','Pagada',750),
('Carlos Flores','Pendiente',300),
('Ana Torres','Anulada',200),
('Luis Ramos','Pagada',900);
GO

INSERT INTO orden_detalle
(orden_id,producto,cantidad,precio_unitario,subtotal)
VALUES
(1,'Teclado',2,100,200),
(1,'Mouse',3,100,300),

(2,'Monitor',1,500,500),
(2,'Cable HDMI',5,50,250),

(3,'Memoria RAM',2,100,200),
(3,'USB',2,50,100),

(4,'Disco SSD',1,150,150),
(4,'Adaptador',1,50,50),

(5,'Laptop',1,800,800),
(5,'Mouse',2,50,100);
GO