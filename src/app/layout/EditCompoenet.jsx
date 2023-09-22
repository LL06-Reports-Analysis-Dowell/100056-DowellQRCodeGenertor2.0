'use client'
import React from 'react'
import {Pencil} from 'lucide-react'
import * as DialogPrimitive from "@radix-ui/react-dialog";
import { Button } from "@/components/ui/button";
import { useState } from 'react';
import { useToast } from "@/components/ui/use-toast";


import {
    Dialog,
    DialogContent,
    DialogDescription,
    DialogHeader,
    DialogTitle,
    DialogTrigger,
  } from "@/components/ui/dialog";
  
const EditCompoenet = (props) => {
    
  // put api function
  const [editing, setEditing] = useState(false);

  const { toast } = useToast();
  let [formData, setFormData] = useState({
    link: props.qrcode.link_,
    word_1: props.qrcode.word,
    word_2: props.qrcode.word2,
    word_3: props.qrcode.word3,
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prevData) => ({
      ...prevData,
      [name]: value,
    }));
  };

  const handleSubmit = async (e) => {
    setEditing(true);

    const id = e.currentTarget.getAttribute("qrcode_ID");

    const apiUrl = `https://www.qrcodereviews.uxlivinglab.online/api/v4/update-qr-code/${id}`;
    const requestData = {
      link: formData.link,
      word: formData.word_1,
      word2: formData.word_2,
      word3: formData.word_3,
    };
    console.log("data", requestData);
    try {
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
        toast({
          title: `URL updatted successfully`,
          className: "text-white btnStyle border-none]",
        });
        props.infoFucntion();
      }   
      if(responseData.error === "Oops! Seems like the words have already been used."){
        setEditing(false);
        toast({
          title: `Oops! Seems like the words have already been used.`,
          className: "text-white btnStyle border-none]",
        });
        props.infoFucntion();
      }
    } catch (error) {
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
                          for="link"
                          class="block text-white text-sm font-bold mb-2"
                        >
                          Master Link
                        </label>
                        <div className="grid grid-cols-4 gap-x-2">
                          <input
                            type="text"
                            placeholder="Readonly Input"
                            className="text-black h-10 px-2 border border-gray-300 rounded-md focus:outline-none focus:ring focus:border-blue-500"
                            readonly
                            value={props.qrcode.link}
                          />

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
                          className=" greenBtn text-white font-bold rounded-md p-5"
                          type="button"
                          onClick={handleSubmit}
                          disabled={editing}
                        >
        {editing ? 'Updating' : 'Update URL'}
                        </Button>
                      </div>
                    </DialogDescription>
                  </DialogHeader>
                </DialogContent>
              </Dialog>
    </div>
  )
}

export default EditCompoenet
