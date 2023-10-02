/* eslint-disable @next/next/no-img-element */
"use client";
import React from "react";
import { QrCode, Copy } from "lucide-react";
import { Button } from "@/components/ui/button";
import * as DialogPrimitive from "@radix-ui/react-dialog";
import EditComponent from './EditComponent'
import SendEmailComponent from './SendEmail'
import { toast } from "react-toastify";
import NotFound from "../../components/notFound"
import { format, parseISO } from 'date-fns';

import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";


const DisplayQRCodes = (props) => {
  const copylink = (e) => {
    const link = e.currentTarget.getAttribute("link");

    navigator.clipboard.writeText(link);
    toast.info("Link Copied")
  };

  const filteredQRCodes = props.qrcodes.filter((q) =>
    q?.name?.toLowerCase().includes(props.searchQuery.toLowerCase())
  );

  return (

    <div className="md:mr-10 md:ml-10">
      {
        filteredQRCodes.length > 0 ?
        filteredQRCodes.map((qrcode, key) => {
        return (
          <div
            key={key}
            className="pb-4 rounded-xl p-3 cardbg  m-4  sm:flex sm:flex-col md:grid md:grid-cols-4 text-white"
          >
            <div className="mr-3 mb-3 md:mb-0 md:mr-0">
              <p className="urlText text-xs">Name</p>
              <p>{qrcode?.name}</p>

              <p className="urlText text-xs">

                {
                  !qrcode?.updated_on ? `created on: ${qrcode?.created_on ? 
                  format(parseISO(qrcode?.created_on), 'MMMM dd yyyy, h:mm a' ) : "-"}` : 
                  `last updated: ${format(parseISO(qrcode?.updated_on), 'MMMM dd yyyy, h:mm a')}`
                }
              </p>

            </div>

            <div className="mr-3 mb-3 md:mb-0 md:mr-0">
              <p className="urlText text-xs">Original URL</p>
              <a href={qrcode?.link_} className="shortenUrl">{qrcode?.link_}</a>
            </div>
            
            <div className="mr-3 mb-3 mr:mr-0">
              <p className="urlText text-xs">Shortened URL</p>
              <a href={qrcode?.link} className="shortenUrl">{qrcode?.link}</a>
            </div>
            
            <div className="flex md:justify-end sm:justify-start items-center">
              {/* qr  modal button  */}
              <Dialog>
                <DialogTrigger>
                  <QrCode className="icon"/>
                </DialogTrigger>
                <DialogContent className="edit modalBg">
                  <DialogHeader>
                    <DialogTitle>
                      Scan Qrcode
                    </DialogTitle>
                    <DialogDescription>
                        <img
                          src={qrcode?.qrcode_image_url}
                          width="auto"
                          height="auto"
                          alt="qr image to scan"
                          className="mx-auto"
                        />
                      {/* <a href={qrcode.qrcode_image_url} className="shortenUrl text-white-400 text-md">
                        {qrcode.qrcode_image_url}
                      </a> */}
                      <div className="flex justify-center gap-x-5 text-center my-5">
                        <DialogPrimitive.Close>
                          <Button className="w-full md:w-auto px-4 py-2 text-black focus:outline-none flex items-center justify-center">
                            Cancel
                          </Button>
                        </DialogPrimitive.Close>
                        <button
                          link={qrcode.qrcode_image_url}
                          className="w-full md:w-auto px-4 py-2 btnStyle text-white font-semibold py-2 px-4 rounded"
                          onClick={copylink}
                        >
                          Copy Qrcode Image Link
                        </button>
                      </div>
                    </DialogDescription>
                  </DialogHeader>
                </DialogContent>
              </Dialog>

              <div className="icon ml-3">
                <SendEmailComponent qrcode={qrcode} infoFucntion={props.getUserInfo} userInfo={props.userInfo}/>
              </div>
              <div className="icon ml-3">
                <EditComponent qrcode={qrcode} infoFucntion={props.getUserInfo}/>
              </div>
              <button className="icon ml-3" link={qrcode.link} variant="outline" onClick={copylink}>
                <Copy />
              </button>
            </div>
          </div>
        );
      }) : <NotFound message={`No Links found with name "${props?.searchQuery}"`} />}
    </div>
  );
};

export default DisplayQRCodes;
