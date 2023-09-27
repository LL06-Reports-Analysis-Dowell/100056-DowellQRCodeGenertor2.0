'use client'
import React from 'react'
import {Pencil} from 'lucide-react'
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
  
const EditComponent = (props) => {
    
  // put api function
  const [editing, setEditing] = useState(false);

  let [formData, setFormData] = useState({
    link: props.qrcode?.link_,
    name:  props.qrcode?.name,
    word_1: props.qrcode?.word,
    word_2: props.qrcode?.word2,
    word_3: props.qrcode?.word3,
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
    
    const apiUrl = `https://www.uxlive.me/api/qrcode/v1/update-qr-code/${id}`;
    const requestData = {
      link: formData.link,
      name: formData?.name,
      word: formData.word_1,
      word2: formData.word_2,
      word3: formData.word_3,
    };
    console.log("data", requestData);
    try {
      setEditing(true);
      const response = await fetch(apiUrl, {
        method: "PUT",

        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(requestData),
      });

      const responseData = await response.json();
      console.log("API response PUT:", responseData); 
      if(responseData.success){
        setEditing(false);
        toast.success(responseData?.success)
        props.infoFucntion();
      }   
      if(responseData.error){
        setEditing(false);
        toast.error(responseData?.error);
        props.infoFucntion();
      }
    } catch (error) {
      setEditing(false);
      console.error(error.message);
    }
  };

  return (
    <div>
       <Dialog>
                <DialogTrigger>
                  <Pencil />
                </DialogTrigger>
                <DialogContent className="text-white modalBg">
                  <DialogHeader>
                    <DialogTitle className="edit text-md font-bold">
                      Edit URL
                    </DialogTitle>
                    <DialogDescription>
                      <div className="container mx-auto p-4">
                        <label
                          for="link"
                          class="block text-white text-sm font-bold mb-2"
                        >
                          Link
                        </label>
                        <input
                          name="link"
                          type="text"
                          id="link"
                          value={formData.link || ""}
                          onChange={handleChange}
                          placeholder="Enter the link here"
                          className="text-black w-full px-3 py-2 border border-gray-300 rounded-xl focus:outline-none focus:ring focus:border-blue-500"
                        />
                      </div>

                      <div className="container mx-auto p-4">
                        <label
                          for="name"
                          class="block text-white text-sm font-bold mb-2"
                        >
                          Name
                        </label>
                        <input
                          name="name"
                          type="text"
                          id="name"
                          value={formData.name || ""}
                          onChange={handleChange}
                          placeholder="Enter the name here"
                          className="text-black w-full px-3 py-2 border border-gray-300 rounded-xl focus:outline-none focus:ring focus:border-blue-500"
                        />
                      </div>

                      <div className="container mx-auto p-4">
                        <label
                          for="link"
                          class="block text-white text-sm font-bold mb-2"
                        >
                          Master Link
                        </label>
                        <div className="grid grid-cols-4 gap-x-2">
                          <input
                            type="text"
                            placeholder="Readonly Input"
                            className="w-full bg-transparent text-white h-10 px-0 border border-transparent rounded-md focus:outline-none focus:none focus:none"
                            readonly
                            value="https://www.qrcodereviews.uxlivinglab.online/"
                          />
                          {/* {props.qrcode.link} */}

                          <input
                            name="word_1"
                            value={formData.word_1 || ""}
                            onChange={handleChange}
                            type="text"
                            placeholder="word1"
                            className=" text-black h-10 px-2 border border-gray-300 rounded-xl focus:outline-none focus:ring focus:border-blue-500"
                          />

                          <input
                            name="word_2"
                            value={formData.word_2 || ""}
                            onChange={handleChange}
                            type="text"
                            placeholder="word2"
                            className="text-black h-10 px-2 border border-gray-300 rounded-xl focus:outline-none focus:ring focus:border-blue-500"
                          />

                          <input
                            name="word_3"
                            value={formData.word_3 || ""}
                            onChange={handleChange}
                            type="text"
                            placeholder="word3"
                            className="text-black h-10 px-2 border border-gray-300 rounded-xl focus:outline-none focus:ring focus:border-blue-500"
                          />
                        </div>
                      </div>
                      <div className="flex justify-center gap-x-5 text-center my-5">
                        <DialogPrimitive.Close>
                          <Button className="greyBtn text-white font-bold rounded-md p-5">
                            Cancel
                          </Button>
                        </DialogPrimitive.Close>
                        <Button
                          qrcode_ID={props.qrcode.qrcode_id}
                          className="greenBtn text-white font-bold rounded-md p-5"
                          type="button"
                          onClick={handleSubmit}
                          disabled={editing}
                        >
                          {editing ? <Loader2 className="mr-2 h-4 w-4 text-4xl animate-spin" /> : 'Update URL'}
                        </Button>
                      </div>
                    </DialogDescription>
                  </DialogHeader>
                </DialogContent>
              </Dialog>
    </div>
  )
}

export default EditComponent
