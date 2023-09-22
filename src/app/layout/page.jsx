"use client";
import React, { useState } from "react";
import DisplayQRCodes from "./DisplayQRCodes";
import { useToast } from "@/components/ui/use-toast";

import { Input } from "@/components/ui/input";
const QRCodeForm = () => {
  const { toast } = useToast();

  const custID = sessionStorage.getItem("custId");
  const userID = sessionStorage.getItem("userId");
  let [displayData, setDisplayData] = useState({});
  const [submitting, setSubmitting] = useState(false);

  let [formData, setFormData] = useState({
    company_id: custID,
    user_id: userID,
    link: "",
  });
  console.log(formData.link);
  console.log("customer", sessionStorage.getItem("custId"));
  console.log("User", sessionStorage.getItem("userId"));

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prevData) => ({
      ...prevData,
      [name]: value,
    }));
  };

  const handleSubmit = async () => {
          setSubmitting(true);

    if (formData.link != "") {


      const apiUrl =
        "https://www.qrcodereviews.uxlivinglab.online/api/v4/qr-code/";
      const requestData = {
        company_id: formData.company_id,
        user_id: formData.user_id,
        link: formData.link,
      };
      console.log("data", requestData);

      try {
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
          toast({
            title: `Link Submitted successfully`,
            className: "text-white btnStyle border-none]",
          });
          formData.link=""
        }
        if (responseData.link) {
          toast({
            title: `Invalid URL`,
            className: "text-white btnStyle border-none]",
          });
        } else {
          await setDisplayData(responseData.qrcode);
          console.log("Put API response", await displayData);
        }
      } catch (error) {
        console.error(error.message);
      }

    } else {
      alert("Link cannot be empty");
    }
  };
  return (
      <div className="m-5 pb-4 grid place-items-center min-h-screen grid grid-cols-1 sm:grid-cols-1 md:grid-cols-[10px,auto,10px] ">
        <div className="px-2"></div>
        <div className=" px-2 h-auto p-5 m-5">
          <div className="mainCard mt-5 h-auto">
            <h1 className="text-2xl mt-5 text-center p-5 text-white font-bold">
              Dowell URL Shortener
            </h1>
            <p className="subText text-center">
              Create short and memorable links in seconds
            </p>
            <div className="container mx-auto p-4 my-5">
              <div className="flex flex-col md:flex-row justify-center items-center space-y-2 md:space-y-0 md:space-x-2">
                <Input
                  type="text"
                  name="link"
                  value={formData.link || ""}
                  onChange={handleChange}
                  placeholder="Enter the link here"
                  className="w-full md:w-1/2 px-4 py-2 bg-white border border-gray-300 rounded-xl focus:outline-none focus:ring focus:border-blue-500"
                />
                <button
                disabled={submitting}
                  type="button"
                  onClick={handleSubmit}
                  className="w-full md:w-auto px-4 py-2 btnStyle text-white rounded-xl focus:outline-none focus:ring"
                >
 {submitting ? 'Processing' : 'Submit'}
                 </button>{" "}
              </div>
            </div>
          
            <DisplayQRCodes/>

          </div>
        </div>
        <div></div>
      </div>
  );
};

export default QRCodeForm;
