import React,{useState,useEffect} from 'react'
import Radiobutton from './Radiobutton'
import Input from './Input'
import Button from './Button'


export default function Addstudent({open}) {
  const [name,setName]=useState("")
  const [email,setEmail]=useState("")
  const [level,setLevel]=useState("")
  const [password,setPassword]=useState("")
  const [file,setFile]=useState("")
  const [addtype,setAddtype]=useState(null)
  var hidden;
  if (addtype==="manual"){
    console.log(addtype)
    hidden=false}
  else if (addtype==="csv"){
    console.log(addtype)
    hidden=true}
  else {hidden=false}


  return (
    <section className={`text-secondary w-full mt-4  `}>
      <p className='text-center ml-5 text-xl lg:text-3xl md:text-2xl w-[80%] sm:w-[60%] md:w-[40%] '>Add student</p>
      <form action="">
        <div  className='flex justify-center text-sm  md:text-md lg:text-lg gap-8 mx-6 mt-4 w-[80%] sm:w-[60%] md:w-[40%] whitespace-pre'>
         
         
          <div>
          <input checked className="hidden" type="radio"  name="group" value="manual" id="A1"  onClick={(e)=>setAddtype(e.target.value)} />
          <label className={` rounded-full bg-secondary text-third p-3 duration-100  ${!hidden && "bg-slate-400 border-2 border-primary"} `} htmlFor="A1">Manual add</label>
          </div>


          <div>
          <input className="hidden" type="radio"  name="group" value="csv" id="A2"  onClick={(e)=>setAddtype(e.target.value)} />
          <label className={` rounded-full bg-secondary text-third p-3 duration-100  ${hidden && "bg-slate-400 border-2 border-primary"}  `}  htmlFor="A2">Add by CSV</label>
          </div>
          </div>
          
          
          
          
          
          <div className={`relative text-center ml-5 mt-12 space-y-4 w-[80%] sm:w-[60%] md:w-[40%] duration-100 ${hidden && 'hidden'} `}>
          <Input
            type={"text"}
            name={"name"}
            label={"Name"}
            state={name}
            set={setName}
          />


            <Input
            type={"text"}
            name={"level"}
            label={"Level"}
            state={level}
            set={setLevel}
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

      <form>

      <div className={`relative text-center ml-5 mt-12 space-y-4 w-[80%] sm:w-[60%] md:w-[40%] duration-100 ${!hidden && 'hidden'} `}>

      <Input
            type={"text"}
            name={"level"}
            label={"Level"}
            state={level}
            set={setLevel}
          />
      <Input
      type={"file"}
      name={"file"}
      label={""}
      state={file}
      set={file}/>
                  
                  
        <div className='pt-4 w-[60%] mx-auto'>
           <Button text={"Submit"}  />
          </div>
      </div>

      </form>
  

    </section>
  )
}
