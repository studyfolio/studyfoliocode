import React,{ useEffect,useState } from 'react'
import SideNavBar from '../components/SideNavBar'
import Addstudent from '../components/Addstudent';



export default function AdminDashboard() {
  useEffect(() => {
    document.title = "Administrator dashboard";
  }, [])
  const [open,setOpen]=useState(false)

  return (

    <div className='flex bg-white'>
    <SideNavBar open={open} setOpen={setOpen} />
    <Addstudent open={open}  />

    </div>
  )
}
