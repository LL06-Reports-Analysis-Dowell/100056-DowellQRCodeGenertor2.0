"use client";
import { useRouter } from "next/navigation";
import { useEffect } from "react";
import { useSearchParams } from "next/navigation";
import {Loader} from './layout/Loader'
 

const HomePage = () => {
  const router = useRouter()
  const searchParams = useSearchParams();
  let dataObject = {
    customerID:"232A",
    userID:"578fhg"
  }
  useEffect(() => {
    const url = `${searchParams}`;
    console.log(url);
    if (!url) {
      console.log("not runn");
      const redirectUrl =
        "https://100014.pythonanywhere.com/en/?redirect_url=" +
        encodeURIComponent(window.location.href);
      if (typeof window !== "undefined") {
        window.location.href = redirectUrl;
      }
    } else {
      const apiUrl = "https://100014.pythonanywhere.com/api/userinfo/";
      async function fetchUserInfo(apiUrl, url) {
        let ret = url.replace("session_id=", "");
        try {
          const response = await fetch(apiUrl, {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({ session_id: ret }),
          });

          if (!response.ok) {
            throw new Error("Network response was not ok");
          }

          const data = await response.json();
          console.log("User:", data);
          if(data.message === "You are logged out, Please login and try again!!"){
            
            router.push( "https://100014.pythonanywhere.com/en/?redirect_url=" +
            encodeURIComponent(window.location.href))
          }
          else{
          dataObject.customerID= data.userinfo.client_admin_id;
          dataObject.userID= data.userinfo.userID
          console.log(dataObject)
          sessionStorage.setItem("User data",data)
          sessionStorage.setItem("custId", dataObject.customerID);
          sessionStorage.setItem("userId", dataObject.userID);
          router.push('/layout')
        }
             } 
        catch (error) {
          console.error("Error fetching user info:", error);
        }
      }

      fetchUserInfo(apiUrl, url);
    }
  }, []);

  // return <QRCodeForm custID={dataObject.customerID} userId={dataObject.userID}/>;
  return <Loader/>
};

export default HomePage;
