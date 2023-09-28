/* eslint-disable react-hooks/exhaustive-deps */
"use client";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import { useSearchParams } from "next/navigation";
import {Loader} from './layout/Loader'
import { toast, ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";

import axios from 'axios'
import QRCodeForm from "./layout/page";


const HomePage = () => {
  const searchParams = useSearchParams();
  const session_id = searchParams.get("session_id");
  const [userInfo, setUserInfo] = useState()

  const getUserInfo = async () => {
    // setLoadingFetchUserInfo(true);
    const session_id = searchParams.get("session_id");
    axios
      .post("https://100014.pythonanywhere.com/api/userinfo/", {
        session_id: session_id
      })

      .then((response) => {
        setUserInfo(response?.data?.userinfo);
        // setLoadingFetchUserInfo(false);
      })
      .catch((error) => {
        // setLoadingFetchUserInfo(false);
        console.error("Error:", error);
      });
  };



  useEffect(() => {
    if (!session_id) {

      window.location.href =
        "https://100014.pythonanywhere.com/en/?redirect_url=" +
        `${window.location.href}`;
      return;
    }
    getUserInfo()
    // setLoggedIn(true);
  }, []);


  return (
    <>
      <ToastContainer
        position="top-right"
        autoClose={5000}
        hideProgressBar={false}
        newestOnTop={false}
        closeOnClick
        rtl={false}
        pauseOnFocusLoss
        draggable
        pauseOnHover
      />
      {userInfo ? <QRCodeForm userInfo={userInfo}/> : <Loader />}
    </>
  
  )
};

export default HomePage;
