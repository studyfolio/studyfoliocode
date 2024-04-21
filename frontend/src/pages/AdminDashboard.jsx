import React,{ useEffect,useState } from 'react'
import SideNavBar from '../components/SideNavBar'
import Addstudent from '../components/Addstudent';
import Addteacher from '../components/Addteacher';



export default function AdminDashboard() {
  useEffect(() => {
    document.title = "Administrator dashboard";
  }, [])
  const [open,setOpen]=useState(false)
  const [currentpage,setCurrentpage]=useState('')
  const set=()=>{
    switch (currentpage) {
      case "Add student":
        return <Addstudent />
        break;
      case "Add teacher":
        return <Addteacher />
    
      default:
        return null
        break;
    }


  }

  return (

    <div className='flex bg-white'>
    <SideNavBar open={open} setOpen={setOpen} setCurrentpage={setCurrentpage} />
    {set()}


    </div>
  )
}
