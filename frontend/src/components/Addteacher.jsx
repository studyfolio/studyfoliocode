import React,{useState} from 'react'
import Input from './Input'
import Button from './Button'


export default function Addteacher() {
    const [name,setName]=useState("")
    const [email,setEmail]=useState("")
    const [grade,setGrade]=useState("")
    const [password,setPassword]=useState("")

   
   
     return (
       <section className={`text-secondary w-full mt-4  `}>
         <p className='text-center ml-5 text-xl lg:text-3xl md:text-2xl w-[80%] sm:w-[60%] md:w-[40%] '>Add teacher</p>
         <form action="">
             <div className={`relative text-center ml-5 mt-8 space-y-4 w-[80%] sm:w-[60%] md:w-[40%] duration-100  `}>
             <Input
               type={"text"}
               name={"name"}
               label={"Name"}
               state={name}
               set={setName}
             />
   
   
               <Input
               type={"text"}
               name={"grade"}
               label={"Grade"}
               state={grade}
               set={setGrade}
             />
               <Input
               type={"email"}
               name={"email"}
               label={"Email"}
               state={email}
               set={setEmail}
             />
   
   
               <Input
               type={"password"}
               name={"password"}
               label={"Password"}
               state={password}
               set={setPassword}
   
   
             />
             <div className='pt-4 w-[60%] mx-auto'>
              <Button text={"Submit"}  />
              </div>
               </div>
              
   
         </form>
     
   
       </section>
     )
}
