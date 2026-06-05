import { auth } from "./firebase.js"; 
import { 
createUserWithEmailAndPassword, 
signInWithEmailAndPassword, 
GoogleAuthProvider, 
signInWithPopup, 
signOut, 
  onAuthStateChanged 
} from "https://www.gstatic.com/firebasejs/12.0.0/firebase-auth.js"; 
 
const provider = new GoogleAuthProvider(); 
 
const email = document.getElementById("email"); 
const password = document.getElementById("password"); 
const status = document.getElementById("status"); 
const userInfo = document.getElementById("userInfo"); 
 
// Register 
document.getElementById("registerBtn").addEventListener("click", async () => { 
  try { 
    await createUserWithEmailAndPassword( 
      auth, 
      email.value.trim(), 
      password.value 
    ); 
 
    status.innerText = "✅ Registration Successful"; 
  } catch (error) { 
 
    if (error.code === "auth/email-already-in-use") { 
      status.innerText = "❌ Email already registered. Please login."; 
    } 
    else if (error.code === "auth/weak-password") { 
      status.innerText = "❌ Password must be at least 6 characters."; 
    } 
    else if (error.code === "auth/invalid-email") { 
      status.innerText = "❌ Invalid email address."; 
    } 
    else { 
      status.innerText = error.message; 
    } 
 
    console.error(error); 
  } 
}); 
 
// Login 
document.getElementById("loginBtn").addEventListener("click", async () => { 
  try { 
    await signInWithEmailAndPassword( 
      auth, 
      email.value.trim(), 
      password.value 
    ); 
 
    status.innerText = "✅ Login Successful"; 

    window.location.href = "/index";

  } catch (error) { 
 
    if ( 
      error.code === "auth/invalid-credential" || 
      error.code === "auth/user-not-found" || 
      error.code === "auth/wrong-password" 
    ) { 
      status.innerText = "❌ Incorrect email or password."; 
    } 
    else { 
      status.innerText = error.message; 
    } 
 
    console.error(error); 
  } 
}); 
 
// Google Login 
document.getElementById("googleBtn").addEventListener("click", async () => { 
  try { 
    await signInWithPopup(auth, provider); 
 
    status.innerText = "✅ Google Login Successful"; 

    window.location.href = "/index";
    
  } catch (error) { 
    status.innerText = error.message; 
    console.error(error); 
  } 
}); 
 
// Logout 
document.getElementById("logoutBtn").addEventListener("click", async () => { 
  try { 
    await signOut(auth); 
 
    status.innerText = "✅ Logged Out"; 
  } catch (error) { 
    status.innerText = error.message; 
    console.error(error); 
  } 
}); 
 
// User State 
onAuthStateChanged(auth, (user) => { 
 
  if (user) { 
 
    userInfo.innerHTML = ` 
      <strong>${user.displayName || "User"}</strong><br> 
      ${user.email} 
    `; 
 
  } else { 
 
    userInfo.innerHTML = "No user logged in"; 
 
  } 
 
});