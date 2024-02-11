/* eslint-disable react/prop-types */
/* eslint-disable react-hooks/exhaustive-deps */
/* eslint-disable @next/next/no-img-element */

import { useEffect, useState } from 'react';
import Button from 'react-bootstrap/Button';
import Modal from 'react-bootstrap/Modal';
import AlertDismissible from './alert';

import axios from 'axios';
import { Loader2 } from "lucide-react"

function OccurenceModal({showModal, setOpenModal, handleFormData, showOccurrence, occurrence, email}) {
  const [hasCoupon, setHasCoupon] = useState(false)
  const [ coupon, setCoupon ] = useState('')
  const [ loading, setLoading ] = useState(false)
  const [ message, setMessage ] = useState({
    warning: false,
    error: false,
    text: ''
  })

  const handleCoupon = () => {
    setHasCoupon(!hasCoupon)
  }

  const handleRedeemCoupon = async () => {
    setLoading(true)
    try {
      // setLoading(true);
      const response = await axios.post(
        `https://100105.pythonanywhere.com/api/v3/experience_database_services/?type=redeem_coupon`,
        {
          email: email,
          coupon:coupon,
          product_number:"UXLIVINGLAB005"
      }
      );
      // Set the emailSent state to true when the email is sent
      setLoading(false);
      console.log(response);

      if (response.data.message == "Coupon is not available") {
        setMessage({
          error: true,
          text: response?.data?.message
        })
      } 

      if (response.data.success == true) {
        setMessage({
          error: false,
          text: `Success. ${response?.data?.message}.`
        })
      } 

    } catch (error) {
      setLoading(false);
      setMessage({
        warning: true,
        text: error?.response?.data?.message
      })

      console.log(error);
    }
  };

  useEffect(() => {
    setMessage(message)
  }, [message])

  return (
    <>
      <Modal centered show={showModal} onHide={() => setOpenModal(false)}>
        {/* <Modal.Header closeButton>
          
        </Modal.Header> */}
        <Modal.Body>

        <div className="modal-divs">
          <img
            style={{width: "100px"}}
            src="https://www.uxlivinglab.org/wp-content/uploads/2023/10/image_1-3.png"
            alt="Dowell Logo"
          />

          <div style={{fontWeight: "bold", fontSize: "20px", align:"center"}}>Dowell URL Shortener</div>
        </div>

        <div className="modal-divs">
          {
            // experience is greater or equal to 6
            showOccurrence &&
            occurrence >= 6 &&
            occurrence !== null ? (
            <>
              <p>Your experience count is {occurrence}!</p>
              <div className="btn-flex">
                <Button className='btn-custom-danger' onClick={() => setOpenModal(false)}>Cancel</Button>
                <Button className='btn-custom-success'>
                  <a 
                    className="btn-link"
                    target="_blank"
                    rel="noopener noreferrer"
                    href='https://dowellpay.online/contribute-payment/?product_number=UXLIVINGLAB005'>
                    Contribute
                  </a>
                </Button>
              </div>
            </>
          ) :
          
          // experience is less than 4
          showOccurrence &&
          occurrence < 4 &&
          occurrence !== null ?
          <>
            <p>Your experience count is {occurrence}!</p>
            <div>
              <Button 
                className='btn-custom-success' 
                onClick={() => {
                  setOpenModal(false);
                  handleFormData();
                }}>
                  Continue
              </Button>
            </div>
          </>

          // experience is greater or equal to 4 and is less than 6
          : 
          showOccurrence &&
            occurrence >= 4 &&
            occurrence < 6 &&
            occurrence !== null && (
              <div>
                <p>Your experience count is {occurrence}!</p>
                <div className='btn-flex'>
                  <Button 
                    className='btn-custom-success ' 
                    onClick={() => {
                      setOpenModal(false);
                      handleFormData();
                    }}>
                      Continue
                  </Button> 
                  
                  <Button className='btn-custom-secondary'>
                    <a 
                      className="btn-link"
                      target="_blank"
                      rel="noopener noreferrer"
                      href='https://dowellpay.online/contribute-payment/?product_number=UXLIVINGLAB005'>
                      Contribute
                    </a>
                  </Button>
                </div>
              </div>
          )
        }
        
        </div>

        { occurrence >= 4 &&
          <div className = "modal-divs" style={{marginTop: "25px", marginBottom: "25px"}}>
            <p>Do you have a coupon? <Button className={hasCoupon ? "btn-custom-danger" : "btn-custom-primary"} onClick={handleCoupon}>{hasCoupon ? "No" : "Yes"}</Button></p>
          </div>
        }

        { 
          hasCoupon && 
          <div>
            <div style={{ display: "flex", gap: "5px"}}>
              <input
                type="text"
                className="form-control"
                value={coupon}
                onChange={(e) => setCoupon(e.target.value)}
                placeholder="Enter Coupon"
              /> 
              <Button 
                className="btn-custom-success"
                disabled={!coupon || loading}
                onClick={handleRedeemCoupon}>
                  {loading ?  <Loader2 className="text-4xl animate-spin" /> : "Redeem"}
              </Button>
            </div>
            <div style={{marginTop: "5px"}}>
              {
                message.text && 
                <AlertDismissible 
                  variant={message?.error ? "danger" : message?.warning ? "warning" : !message?.error && "success"}
                  message={message?.text} 
                />}
            </div>
          </div>
        }
        </Modal.Body>
      </Modal>
    </>
  );
}

export default OccurenceModal;