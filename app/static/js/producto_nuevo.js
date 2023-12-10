function guardar() {
    let cantidad = parseInt(document.getElementById('cantidad').value)
    let categoria = document.getElementById('categoria').value
    let codigo = parseInt(document.getElementById('codigo').value)
    let descripcion = document.getElementById('descripcion').value
    let precioUnit = parseFloat(document.getElementById('precioUnit').value)
    let precioVPublico = parseFloat(document.getElementById('precioVPublico').value)

    let producto = {
        cantidad: cantidad,
        categoria: categoria,
        codigo: codigo,
        descripcion: descripcion,
        precioUnit: precioUnit,
        precioVPublico: precioVPublico
    }
    let url = "{{ url_for('productos') }}"
    var options = {
        body: JSON.stringify(producto),
        method: 'POST',
        Headers: { 'content-Type': 'application/json' },
    }
    fetch(url, options)
        .then(function() {
            alert("Grabado")
            window.location.href = "productos/tablaadmin";
        })
        .catch(err => {
            alert("Error al Grabar")
            console.error(err)
        })

}