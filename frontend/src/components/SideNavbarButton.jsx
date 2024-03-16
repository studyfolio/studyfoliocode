import React from 'react'

export default function SideNavbarButton({text,icon:Icon,state,margin}) {
  return (
    <button  className={`cursor-pointer flex items-center ${margin && 'mt-10'} gap-3.5 p-2 text-md font-medium rounded-lg hover:bg-third hover:text-secondary `}>
    <div className='duration-200'><Icon size={30} /></div>
    <h1 className={`whitespace-pre ${!state && "hidden  "}`}>{text} </h1>
  </button>  
  
  )
}
