function Message({type, message}){
    var content = document.createElement('div')
    content.classList.add(type=="ok" ?"bg-success":'bg-danger')
    content.classList.add('p-2')

    content.innerText = message

    content.addEventListener('click', function(e){
        this.remove()
    })
    
    content.style.position = 'fixed'
    content.style.top = '0'
    content.style.right = '0'
    content.style.width = '40%'
    content.style.zIndex = '9999'
    content.style.fontSize = '16px'
    content.style.color = 'white'

    document.body.prepend(content)

    setTimeout(() => {
        content.remove()
    }, 8000);
}