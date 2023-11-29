const openBtn = document.querySelector(".js-open")
const modalBG = document.querySelector(".modal-bg")
const modalBox = document.querySelector(".modal-box")

openBtn.addEventListener('click', function(event) {
    event.preventDefault()
    // preventDefault() tells browser to NOT do normal function of event
    console.log('click works')
    modalBox.classList.add('active')
    modalBG.classList.add('active')
})

const closeModal = document.querySelectorAll(".js-close")

closeModal.forEach(node => {
    node.addEventListener('click', function(e) {
        console.log('closed')
        e.preventDefault()
        modalBox.classList.remove('active')
        modalBG.classList.remove('active')
    })
})


