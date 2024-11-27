const API_BASE_ROUTE = "https://phonebook-api-dgus.onrender.com"
// const API_BASE_ROUTE = "http://127.0.0.1:5000"

const loginForm = document.querySelector('#login-form')
loginForm.addEventListener('submit', (event)=>{
  handleLogin(event)
})

const handleLogin = async (e)=> {
  e.preventDefault()
  const email = document.querySelector("input[name='email']").value;
  const password = document.querySelector("input[name='password']").value;
  const preTag = document.querySelector('#pre')
  preTag.innerHTML = "{'response':'waiting..'}"
  try {
  // const res = await axios.get("http://127.0.0.1:5000/api/user/")
  const res = await axios.get(API_BASE_ROUTE + "/api/user/")
  alert('done')
  preTag.innerHTML = JSON.stringify(res.data)
  } catch(e){
    console.log(e)
  }
}