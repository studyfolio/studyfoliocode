import React,{useState} from 'react'
import { IoPersonAddOutline } from "react-icons/io5";
import { HiOutlineMenuAlt2 } from "react-icons/hi";
import { BsPersonGear } from "react-icons/bs";

import SideNavbarButton from './SideNavbarButton';


export default function SideNavBar() {

    


    const [open,setOpen]=useState(true)


  return (
    <nav className={`text-third duration-300 bg-secondary min-h-screen relative ${open ? ' pl-6 pr-8 w-full md:w-72' : 'px-4 w-20 md:w-24 md:px-6'} `}>
      
      <div className={`cursor-pointer py-3 flex justify-end mt-4 ${open && 'mr-6'} md:mr-0 `}>
      <HiOutlineMenuAlt2 size={40} onClick={()=>setOpen(!open)} className={``} />

      </div>
      <div className='flex flex-col mt-8 gap-4 relative'>
      <SideNavbarButton text={"Add student"} icon={IoPersonAddOutline} state={open} margin={false}  />
      <SideNavbarButton text={"Modify student"} icon={BsPersonGear} state={open} margin={false}  />
      <SideNavbarButton text={"Add teacher"} icon={IoPersonAddOutline} state={open} margin={true}  />
      <SideNavbarButton text={"Modify teacher"} icon={BsPersonGear} state={open} margin={false}  />




      </div>
      
    </nav>
  )
}
