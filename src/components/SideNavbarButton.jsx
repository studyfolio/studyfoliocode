import React from 'react'

export default function SideNavbarButton({text,icon:Icon,state,margin}) {
  return (
    <div  className={`cursor-pointer relative flex items-center ${margin && 'mt-10'} gap-3.5 p-2 text-md font-medium rounded-lg hover:bg-third hover:text-secondary `}>
    <div className='duration-200'><Icon size={30} /></div>
    <h1 className={`whitespace-pre duration-200 ${!state && "opacity-0 "}`}>{text} </h1>

  </div>  
  
  )
}
