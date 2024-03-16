import React,{useState} from 'react'
import SideNavbarButton from './SideNavbarButton';
import { IoPersonAddOutline } from "react-icons/io5";
import { HiOutlineMenuAlt2 } from "react-icons/hi";
import { BsPersonGear } from "react-icons/bs";
import { BiLogOut } from "react-icons/bi";
import { Link } from 'react-router-dom';


export default function SideNavBar({open,setOpen}) {

  
  return (
    <nav className={`text-third duration-300 bg-secondary min-h-screen relative ${open ? ' pl-6 pr-8 w-[80%] md:w-72' : 'px-4 w-20 md:w-24 md:px-6'} `}>
      
      <div className={`cursor-pointer py-3 flex justify-end mt-4 ${open && 'mr-6'} md:mr-0 `}>
      <HiOutlineMenuAlt2 size={40} onClick={()=>setOpen(!open)} />
      </div>


      <div className='flex flex-col mt-4 gap-4 relative'>
      <SideNavbarButton text={"Add student"} icon={IoPersonAddOutline} state={open} margin={false}   />
      <SideNavbarButton text={"Modify student"} icon={BsPersonGear} state={open} margin={false}   />
      <SideNavbarButton text={"Add teacher"} icon={IoPersonAddOutline} state={open} margin={true}   />
      <SideNavbarButton text={"Modify teacher"} icon={BsPersonGear} state={open} margin={false}   />
      </div>
  

      <Link to={'/'}  className={`fixed bottom-6 cursor-pointer flex items-center gap-3.5 p-2 text-md font-medium rounded-lg hover:bg-third hover:text-secondary `}>
      <div className='duration-200'><BiLogOut size={30} /></div>
      <h1 className={`whitespace-pre duration-200 ${!open && "hidden"} `}>Logout </h1>
      </Link>
    
    </nav>
  )
}
