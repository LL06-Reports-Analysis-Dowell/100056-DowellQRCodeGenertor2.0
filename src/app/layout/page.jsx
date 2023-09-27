/* eslint-disable @next/next/no-img-element */
"use client";
import React, { useState, useEffect } from "react";
import { useSearchParams } from "next/navigation";
import DisplayQRCodes from "./DisplayQRCodes";
import { toast } from "react-toastify";
import { Loader2 } from "lucide-react"
import { Input } from "@/components/ui/input";
import { Loader } from "./Loader";
import NotFound from "../../components/notFound"
import Link from "next/link";

const QRCodeForm = ({userInfo}) => {
  // get api 
  const [qrcodes, setQRCodes] = useState();
  const [loading, setLoading] = useState(false)
   

  const fetchQrCodes = async () => {
    const apiUrl = `https://uxlivinglab100106.pythonanywhere.com/api/qrcode/v1/qr-code/?user_id=${userInfo?.userID}`;

    try {
      setLoading(true)
      const response = await fetch(apiUrl);

      const responseData = await response.json();
      console.log("status", responseData.ok);
      setQRCodes(responseData?.response?.data);
      setLoading(false)
    } catch (error) {
      setLoading(false)
      console.error(error.message);
    }
  };


  useEffect(() => {
    fetchQrCodes();
  }, []);

  // post api 
  let [displayData, setDisplayData] = useState({});
  const [submitting, setSubmitting] = useState(false);

  let [formData, setFormData] = useState({
    company_id: userInfo?.client_admin_id,
    user_id: userInfo?.userID,
    link: "",
    name: "",
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prevData) => ({
      ...prevData,
      [name]: value,
    }));
  };

  const handleSubmit = async () => {
    
    if (formData.link != "") {
      const apiUrl =
      `https://uxlive.me/api/qrcode/v1/qr-code/`
      const requestData = {
        company_id: formData.company_id,
        user_id: formData.user_id,
        link: formData.link,
        name: formData.name,
      };
      try {
        setSubmitting(true);
        const response = await fetch(apiUrl, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(requestData),
        });

        const responseData = await response.json();

        console.log("API response:", responseData);
        if(responseData.success){
          setSubmitting(false);
          toast.success(`Link Shortened Successfully`);
          formData.link=""
          fetchQrCodes()
        }
        if (responseData.link) {
          toast.info(`Enter a valid URL`);
          setSubmitting(False)
        } else if (responseData.name) {
          toast.info(`Name is required`);
          setSubmitting(False)
        } else {
          setSubmitting(False)
          await setDisplayData(responseData.qrcode);
          console.log("Put API response", await displayData);
        }
      } catch (error) {
        setSubmitting(false);
        console.error(error.message);
      }

    } else {
      setSubmitting(false)
    }
  };

  
  
  return (

        <>
          
          <div>
            <div class="navBar fixed top-0 left-0 right-0 p-4 flex justify-between items-center">
              <div class="flex items-center">
                {/* <span class="text-white font-semibold">Your Name</span> */}
              </div>
              <Link 
                href="https://100014.pythonanywhere.com/en-gb/sign-out"
                class="bg-red-900 hover:bg-red-600 text-white font-semibold py-2 px-4 rounded">
                Logout
              </Link>
            </div>

            <div className="flex flex-col justify-center items-center  rounded-lg overflow-auto">
              <img src="message.svg" alt="Your Name" class="text-center mt-10" />
              <h1 className="text-2xl text-center text-white font-bold">
                Welcome to Dowell URL Shortener <span className="name">{userInfo?.first_name}</span>
              </h1>
              <p className="subText text-center">
                Create short and memorable links in seconds
              </p>
            </div>

            <div className="pb-8 w-screen rounded-lg overflow-auto">
              <div className="container mx-auto p-4 my-5">
                <div className="flex flex-col md:flex-row justify-center items-center space-y-2 md:space-y-0 md:space-x-2">
                  <div className="flex flex-col md:flex-row w-full md:w-1/2 space-y-2 md:space-y-0 md:space-x-2">
                    <Input
                      type="text"
                      name="name"
                      value={formData.name || ""}
                      onChange={handleChange}
                      placeholder="Name"
                      className="w-full md:w-1/3 px-4 py-2 bg-white border border-gray-300 rounded-xl focus:outline-none focus:ring focus:border-blue-500"
                    />
                    
                    <Input
                      type="text"
                      name="link"
                      value={formData.link || ""}
                      onChange={handleChange}
                      placeholder="Enter the link here"
                      className="w-full md:w-2/3 px-4 py-2 bg-white border border-gray-300 rounded-xl focus:outline-none focus:ring focus:border-blue-500 justify-center items-center space-y-2"
                    />
                    
                  </div>
                  
                  <button
                    disabled={submitting || formData.link === "" || formData.name === ""}
                    type="button"
                    onClick={handleSubmit}
                    className="w-full md:w-auto px-4 py-2 btnStyle text-white rounded-xl focus:outline-none focus:ring flex items-center justify-center"
                  >
                    {submitting ? <Loader2 className="text-4xl animate-spin" /> : 'Submit'}
                  </button>{" "}
                </div>
              </div>
            </div>

            <div className="pb-8 w-screen rounded-lg overflow-auto">
              {loading ? <Loader /> : qrcodes?.length > 0 ? <DisplayQRCodes qrcodes={qrcodes} getUserInfo={fetchQrCodes}/> : <NotFound />}
            </div>
            
          </div>
        </>
  );
};

export default QRCodeForm;
