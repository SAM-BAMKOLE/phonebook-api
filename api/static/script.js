const devMode = false
const API_BASE_ROUTE = devMode ? "http://localhost:5000" : "https://phonebook-api-dgus.onrender.com"

const navList = document.querySelector('#nav-list')
  const menuBtn = document.querySelector('.menu')
  
  menuBtn.addEventListener("click", ()=> {
    navList.classList.toggle('hidden')
  })
  
function removeAlert() {
  const alertBtn = document.querySelector("#remove-alert")
  const alertDiv = document.querySelector("#alert")
  
  alertDiv.remove()
}
