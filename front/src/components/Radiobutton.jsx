import React from 'react'

export default function Radiobutton({text,id,name,value,set}) {
  return (
    <div>
        <input className="peer hidden" type="radio" name={name} value={value} id={id} onChange={(e)=>set(e.target.value)} />
        <label className=" rounded-full bg-secondary text-third p-3 duration-100  peer-checked:bg-slate-400 peer-checked:border-2 peer-checked:border-primary" htmlFor={id}>{text}</label>
    </div>
  )
}
