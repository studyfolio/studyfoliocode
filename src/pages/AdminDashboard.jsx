import React from 'react'
import SideNavBar from '../components/SideNavBar'
import Addstudent from './Addstudent'
export default function AdminDashboard() {
  return (
    <div className='flex gap-6 bg-third'>
    <SideNavBar />
    <Addstudent />
    </div>
  )
}
