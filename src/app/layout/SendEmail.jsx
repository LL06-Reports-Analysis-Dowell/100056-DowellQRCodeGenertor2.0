'use client'
import React from 'react'
import {Pencil, Send} from 'lucide-react'
import * as DialogPrimitive from "@radix-ui/react-dialog";
import { Button } from "@/components/ui/button";
import { useState } from 'react';
import { toast } from "react-toastify";
import { Loader2 } from "lucide-react"


import {
    Dialog,
    DialogContent,
    DialogDescription,
    DialogHeader,
    DialogTitle,
    DialogTrigger,
  } from "@/components/ui/dialog";
  
const SendEmailComponent = (props) => {
    
  // put api function
  const [sending, setSending] = useState(false);

  let [formData, setFormData] = useState({
    fromName:  `${props.userInfo?.first_name} ${props.userInfo?.last_name}`,
    fromEmail: props.userInfo?.email,
    email: "",
    name: "",
    subject: "Link Shortener",
    body: "This link will take you to a page where you access the information you need. You can also scan the Qrcode attached.",
    api_key: "",
    qrcode_image_url: props?.qrcode?.qrcode_image_url,
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prevData) => ({
      ...prevData,
      [name]: value,
    }));
  };

  

  const handleSubmit = async (e) => {
    const id = e.currentTarget.getAttribute("qrcode_ID");
    
    const apiUrl = `https://100085.pythonanywhere.com/api/v1/mail/${formData.api_key}/?type=send-email`;
    const requestData = {
      fromName: formData?.fromName,
      fromEmail: formData?.fromEmail,
      name: formData?.name,
      email: formData?.email,
      subject: formData?.subject,
      body: formData?.body
    };

    const htmlContent = `
        <!DOCTYPE html>
        <html lang="en">
        <head>
        <meta charset="UTF-8">
        <title>Email Template</title>
        </head>
        <body>
            <p style="color: #000000;">${requestData?.body}</p><br>
            <a href=${props?.qrcode?.link}>${props?.qrcode?.link}</a><br>
            <img style="width: 250px; height: auto;" src=${formData?.qrcode_image_url} alt="Attached Image" />
        </body>
        </html>
    `;
    requestData.body = htmlContent;
    console.log("data", requestData);
    try {
      setSending(true);
      const response = await fetch(apiUrl, {
        method: "POST",

        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(requestData),
      });

      const responseData = await response.json();
      console.log("API response PUT:", responseData); 

      if(responseData.success == true){
        setSending(false);
        toast.success(`${responseData?.message}. ${responseData?.credits} credits remaining.`)
        // props.infoFucntion();
      }   

      if(responseData.success == false){
        setSending(false);
        toast.error(responseData?.message);
      }
    } catch (error) {
      setSending(false);
      console.log(error);
    }
  };

  return (
    <div>
       <Dialog>
        <DialogTrigger>
          <Send />
        </DialogTrigger>

        <DialogContent className="text-white modalBg">
          <DialogHeader>
            <DialogTitle className="edit text-md mb-3 font-bold">
              Share Link
            </DialogTitle>

            <DialogDescription>
              <div className='mb-2'>
                <label
                  for="api_key"
                  className="block edit text-sm font-bold mb-1"
                >
                  Api Key
                </label>
                <input
                  name="api_key"
                  type="text"
                  id="api_key"
                  value={formData.api_key || ""}
                  onChange={handleChange}
                  placeholder="Enter Your Api Key"
                  className="text-black w-full px-3 py-2 border border-gray-300 rounded-xl focus:outline-none"
                />
              </div>


              <div className='mb-2'>
                <label
                  for="fromName"
                  class="block edit text-white text-sm font-bold mb-1"
                >
                  From
                </label>
                <input
                  name="fromName"
                  type="text"
                  id="fromName"
                  value={formData.fromName || ""}
                  // onChange={handleChange}
                  readonly
                  placeholder="Enter Your Name"
                  className="text-black w-full px-3 py-2 border border-gray-300 rounded-xl focus:outline-none cursor-not-allowed pointer-events-none"
                />
              </div>

              <div className="mb-2">
                <input
                  name="fromEmail"
                  type="fromEmail"
                  id="fromEmail"
                  placeholder="Enter Your Email"
                  readonly
                  value={formData.fromEmail || ""}
                  className="text-black w-full px-3 py-2 border border-gray-300 rounded-xl focus:outline-none cursor-not-allowed pointer-events-none"
                />
              </div>

              <div className="mb-2">
                <label
                  for="name"
                  class="block edit text-sm font-bold mb-1"
                >
                  To
                </label>
                <input
                  name="name"
                  placeholder='Enter Recepient Name'
                  type="text"
                  id="name"
                  value={formData.name || ""}
                  onChange={handleChange}
                  className="text-black w-full px-3 py-2 border border-gray-300 rounded-xl focus:outline-none  focus:border-green-500"
                />
              </div>

              <div className="mb-2">
                <input
                  name="email"
                  type="email"
                  id="email"
                  placeholder='Enter Recepient Email'
                  value={formData.email || ""}
                  onChange={handleChange}
                  className="text-black w-full px-3 py-2 border border-gray-300 rounded-xl focus:outline-none  focus:border-green-500"
                />
              </div>

              <div className="mb-2">
                <p className="text-xs text-gray-500 mt-1 ml-1">Email Subject</p>
                <input
                  name="subject"
                  type="subject"
                  id="subject"
                  placeholder='Email Subject'
                  value={formData.subject || ""}
                  onChange={handleChange}
                  className="text-black w-full px-3 py-2 border border-gray-300 rounded-xl focus:outline-none  focus:border-green-500"
                />
              </div>

              <div className="mb-2">
                <p className="text-xs text-gray-500 mt-2 ml-1">Email Body</p>
                <textarea
                  name="body"
                  type="body"
                  id="body"
                  placeholder='Body'
                  value={formData.body || ""}
                  onChange={handleChange}
                  className='text-black w-full h-32 p-4 border border-gray-300 rounded-xl focus:outline-none  focus:border-green-500 resize-y align-top'
                />
              </div>

                
              <div className="flex justify-center gap-x-5 text-center my-5">
                <DialogPrimitive.Close>
                  <Button className="w-full md:w-auto px-4 py-2 text-black focus:outline-none  flex items-center justify-center">
                    Cancel
                  </Button>
                </DialogPrimitive.Close>
                <button
                  // qrcode_ID={props.qrcode.qrcode_id}
                  className="w-full md:w-auto px-4 py-2 btnStyle text-white font-semibold py-2 px-4 rounded"
                  type="button"
                  onClick={handleSubmit}
                  disabled={sending || formData.api_key === "" || formData.name === "" || formData.email === ""}
                >
                  {sending ? <Loader2 className="mr-2 h-4 w-4 text-4xl animate-spin" /> : 'Send Link'}
                </button>
              </div>
            </DialogDescription>
          </DialogHeader>
        </DialogContent>
      </Dialog>
    </div>
  )
}

export default SendEmailComponent
