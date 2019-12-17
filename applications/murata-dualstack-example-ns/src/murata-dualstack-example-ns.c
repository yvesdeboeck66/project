/* USER CODE BEGIN Header */
/**
  ******************************************************************************
  * @file           : main.c
  * @brief          : Main program body
  ******************************************************************************
  * This notice applies to any and all portions of this file
  * that are not between comment pairs USER CODE BEGIN and
  * USER CODE END. Other portions of this file, whether 
  * inserted by the user or by software development tools
  * are owned by their respective copyright owners.
  *
  * Copyright (c) 2019 STMicroelectronics International N.V. 
  * All rights reserved.
  *
  * Redistribution and use in source and binary forms, with or without 
  * modification, are permitted, provided that the following conditions are met:
  *
  * 1. Redistribution of source code must retain the above copyright notice, 
  *    this list of conditions and the following disclaimer.
  * 2. Redistributions in binary form must reproduce the above copyright notice,
  *    this list of conditions and the following disclaimer in the documentation
  *    and/or other materials provided with the distribution.
  * 3. Neither the name of STMicroelectronics nor the names of other 
  *    contributors to this software may be used to endorse or promote products 
  *    derived from this software without specific written permission.
  * 4. This software, including modifications and/or derivative works of this 
  *    software, must execute solely and exclusively on microcontroller or
  *    microprocessor devices manufactured by or for STMicroelectronics.
  * 5. Redistribution and use of this software other than as permitted under 
  *    this license is void and will automatically terminate your rights under 
  *    this license. 
  *
  * THIS SOFTWARE IS PROVIDED BY STMICROELECTRONICS AND CONTRIBUTORS "AS IS" 
  * AND ANY EXPRESS, IMPLIED OR STATUTORY WARRANTIES, INCLUDING, BUT NOT 
  * LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY, FITNESS FOR A 
  * PARTICULAR PURPOSE AND NON-INFRINGEMENT OF THIRD PARTY INTELLECTUAL PROPERTY
  * RIGHTS ARE DISCLAIMED TO THE FULLEST EXTENT PERMITTED BY LAW. IN NO EVENT 
  * SHALL STMICROELECTRONICS OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
  * INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
  * LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, 
  * OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF 
  * LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING 
  * NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE,
  * EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
  *
  ******************************************************************************
  */
/* USER CODE END Header */

/* Includes ------------------------------------------------------------------*/
#include "murata-dualstack-example-ns.h"

/* Private includes ----------------------------------------------------------*/
/* USER CODE BEGIN Includes */
//#include "murata.h"
#include <LSM303AGRSensor.h>
#include <stdio.h>
#include <murata.h>
//#include "murata.h"

/* USER CODE END Includes */

/* Private typedef -----------------------------------------------------------*/
/* USER CODE BEGIN PTD */

/* USER CODE END PTD */

/* Private define ------------------------------------------------------------*/
/* USER CODE BEGIN PD */
#define IWDG_INTERVAL           5    //seconds
#define LORAWAN_INTERVAL        60   //seconds
#define DASH7_INTERVAL          20  //seconds
#define MODULE_CHECK_INTERVAL   3600 //seconds

#define HAL_EXTI_MODULE_ENABLED
#define temp_hum_timer    3

/* USER CODE END PD */

/* Private macro -------------------------------------------------------------*/
/* USER CODE BEGIN PM */

/* USER CODE END PM */

/* Private user code ---------------------------------------------------------*/
/* USER CODE BEGIN 0 */
uint16_t LoRaWAN_Counter = 0;
uint16_t DASH7_Counter = 0;
uint8_t murata_init = 0;
uint64_t short_UID;
uint8_t murata_data_ready = 0;

//Zelf
uint8_t rep_counter = 0; 
extern volatile uint8_t failureCounter=0; 
extern volatile uint8_t successCounter=0;
extern volatile uint8_t messageCounter=0; 

float SHTData[2];
uint8_t tmpbuf_ble[10];
uint8_t data; 
volatile _Bool temperatureflag=0; 
volatile _Bool timer2flag=0; 
volatile _Bool timer3flag=0; 
volatile _Bool repFlag=0;
volatile _Bool repMode=0; 
_Bool changeAcceleroMode=0; 
_Bool volatile messageMode=0; 
volatile _Bool timer3_first=0; 
volatile _Bool BLE_flag=0;


/* USER CODE END 0 */


 
static TIM_HandleTypeDef localisation_timer = { 
    .Instance = TIM2
};

static TIM_HandleTypeDef inactive_timer = { 
    .Instance = TIM3
};
 
void InitializeTimer2()
{
    __TIM2_CLK_ENABLE();
    localisation_timer.Init.Prescaler = 16000;                            //1 step = clockperiod x prescaler
    localisation_timer.Init.CounterMode = TIM_COUNTERMODE_UP;             //timer will count up
    localisation_timer.Init.Period = 60000;                                 //60000 steps of clockperiodxprescaler before the timer resets. we want 1min, but it always gives 1.07. 
    localisation_timer.Init.ClockDivision = TIM_CLOCKDIVISION_DIV1;
    localisation_timer.Init.RepetitionCounter = 0;
   /*  HAL_TIM_Base_Init(&localisation_timer);
    HAL_TIM_Base_Start_IT(&localisation_timer);
    HAL_NVIC_SetPriority(TIM2_IRQn, 0, 0);                              //set de priority of the interrupt van timer2
    HAL_NVIC_EnableIRQ(TIM2_IRQn);        */                               //enable de interrupt van timer2 
} 

void InitializeTimer3()
{
    __TIM3_CLK_ENABLE();
    inactive_timer.Init.Prescaler = 16000;                            //1 step = clockperiod x prescaler
    inactive_timer.Init.CounterMode = TIM_COUNTERMODE_UP;             //timer will count up
    inactive_timer.Init.Period = 60000;                                 //60000 steps of clockperiodxprescaler before the timer resets. we want 1min, but it always gives 1.07. 
    inactive_timer.Init.ClockDivision = TIM_CLOCKDIVISION_DIV1;
    inactive_timer.Init.RepetitionCounter = 0;
    /* HAL_TIM_Base_Init(&inactive_timer);
    HAL_TIM_Base_Start_IT(&inactive_timer);
    HAL_NVIC_SetPriority(TIM3_IRQn, 0, 0); 
    HAL_NVIC_EnableIRQ(TIM3_IRQn); */
}

/**
  * @brief  The application entry point.
  * @retval int
  */
int main(void)
{
  /* USER CODE BEGIN 1 */

  /* USER CODE END 1 */

  /* MCU Configuration--------------------------------------------------------*/

  /* Reset of all peripherals, Initializes the Flash interface and the Systick. */
  HAL_Init();

  /* USER CODE BEGIN Init */

  /* USER CODE END Init */

  /* Configure the system clock */
  SystemClock_Config();

  /* USER CODE BEGIN SysInit */

  /* USER CODE END SysInit */

  /* Initialize the platform, OCTA in this case */
  Initialize_Platform();

  /* Initialize the the timer */
  InitializeTimer2();
  InitializeTimer3(); 

  /* USER CODE BEGIN 2 */

  // Get Unique ID of octa
  short_UID = get_UID();

  //LSM30AGR (accelerometer)
  LSM303AGR_setI2CInterface(&common_I2C);
  setI2CInterface_SHT31(&common_I2C);
  SHT31_begin(); 
  LSM303AGR_initDefault();

  //initialize BLE
  HAL_UART_Receive_IT(&BLE_UART, (uint8_t *)tmpbuf_ble, 10); 

  /* EXTI interrupt init*/
  HAL_NVIC_SetPriority(EXTI1_IRQn, 0, 0);
  HAL_NVIC_EnableIRQ(EXTI1_IRQn);

  // Print Welcome Message
  printWelcome();
  
  // LORAWAN
  murata_init = Murata_Initialize(short_UID, 0);

  if (murata_init)
  {
    printf("Murata dualstack module init OK\r\n\r\n");
  }


  /* USER CODE END 2 */

  /* USER CODE BEGIN RTOS_MUTEX */
  /* add mutexes, ... */

  // TX MUTEX ensuring no transmits are happening at the same time

  /* USER CODE END RTOS_MUTEX */

  /* USER CODE BEGIN RTOS_SEMAPHORES */
  /* add semaphores, ... */
  /* USER CODE END RTOS_SEMAPHORES */

  /* Create the thread(s) */

  /* USER CODE BEGIN RTOS_TIMERS */
  /* start timers, add new ones, ... */

  //feed IWDG every 5 seconds
  //IWDG_feed(NULL);

  /* USER CODE END RTOS_TIMERS */

  /* USER CODE BEGIN RTOS_THREADS */
  /* add threads, ... */

  /* USER CODE END RTOS_THREADS */

  /* USER CODE BEGIN RTOS_QUEUES */
  /* add queues, ... */
  /* USER CODE END RTOS_QUEUES */

  /* Start scheduler */

  /* We should never get here as control is now taken by the scheduler */
  //HAL_Delay(10000);
  /* Infinite loop */
  uint8_t counter = 0;
  uint8_t use_lora = 1;
  uint8_t timerValue = 0; 
  /* USER CODE BEGIN WHILE */
  while (1)
  { 
     IWDG_feed(NULL);
    //HAL_Delay(5000);
    if(murata_data_ready)
    {
      printf("processing murata fifo\r\n");
      murata_data_ready = !Murata_process_fifo();
    }


    //------gekopieerd van no-scheduler-example------
     IWDG_feed(NULL); 
    
    //LSM303AGR_readRegister(0x31, data, 0);

    //als op de button wordt gedrukt zal in de interrupthandler de changeAcceleroMode op 1 worden gezet. 
    if(changeAcceleroMode==1){

      if(repMode==1){
        // send dash7 message with all info when user starts repping
        LSM303AGR_initDouble();         //vanaf laten we de accelorometer enkel interrupten bij een rep beweging
        printf("Started Repping\r\n");
        printf("LSM in double click mode \r\n");
        if (murata_init) {
          printf("Sending D7 Message with BLE info + temp + hum\r\n");
          temp_hum_measurement();
          send_message(1);
          //LoRaWAN_send(NULL);
          printf("Failure counter = %d\r\n",failureCounter);

        //TODO: Send BLE info
        }
        
      }else{
        // send dash7 message with all info when user stopped repping
        LSM303AGR_initDefault();    //vanaf nu laten we de accelerometer interrupten bij elke beweging
        printf("Stopped Repping\nLSM in default mode \r\n\n");
        if (murata_init) {
          printf("Sending D7 Message with BLE info + temp + hum + amount of reps\r\n");
          temp_hum_measurement();
        //Dash7_send_temphum();
          send_message(2); 
          //LoRaWAN_send(NULL);

        //TODO: Also send BLE info and reps

        //Set reps to zero again, for the next user
        }
        rep_counter=0;  //reset the rep counter
      }
      changeAcceleroMode=0; //set acceleromode flag back to zero

    }

    //de interrupt zal zorgen dat de flag op 1 staat, dan doen we een measurement van temp
    if (repFlag==1) {
      if (repMode==1) {
      // Request to enter SLEEP mode
      timerValue = __HAL_TIM_GET_COUNTER(&localisation_timer);
      printf("Timer value: %d,\r\n\r\n",timerValue);
      rep_counter++; 
      printf("Rep counter: %d,\r\n\r\n",rep_counter);

      } 
        //reset de inactive timer want accelerometer interrupt
        // HAL_TIM_Base_Stop_IT(&inactive_timer);    
 

      //  __HAL_TIM_SET_COUNTER(&inactive_timer, 0);
 

        //HAL_TIM_Base_Start_IT(&inactive_timer);         

      
      
          repFlag=0; 
    }  



    if(timer2flag==1) {
       //send dash7 localisation message
      if (murata_init) {
        printf("Sending dash7 localisation message (once per minute)\r\n\r\n");
          temp_hum_measurement();
        send_message(1);
         
      }
     timer2flag=0;
    }
    // go to sleep
     if(timer3flag==1) {
      
      if (murata_init) {
        
        printf("Sending dash7 go to sleep message (once per minute)\r\n\r\n");
        temp_hum_measurement();
        send_message(1); 
        goToSleep(); 
      }
     timer3flag=0;
    } 

    if (failureCounter==3) {
      printf("Going to LoRaWAN mode\r\n\r\n");
      messageMode=1;      //go to lorawanmode
      successCounter=0;
      failureCounter=4; 
    }

     if (successCounter==1) {
      printf("Going to dash7 mode\r\n\r\n");
      messageMode=0;    //go to dash7mode
      successCounter=2;     //step over the 1 value so that between messages this if isn't accessed with every iteration of the while loop
    }


    if (BLE_flag) {
      ble_callback(); 
      BLE_flag = 0; 
      printf("callback flag \r\n");
    }

    // SEND 5 D7 messages, every 10 sec.
    // Afterwards, send 3 LoRaWAN messages, every minute
   /*  if(DASH7_Counter<5)
    {
      if(counter==DASH7_INTERVAL)
      {
        Dash7_send(NULL);
        counter = 0;
      }
    }
    else
    { 
      if(LoRaWAN_Counter == 0)
        Murata_LoRaWAN_Join();
      if(LoRaWAN_Counter<3)
      {
        if (counter == LORAWAN_INTERVAL)
        {
          LoRaWAN_send(NULL);
          counter = 0;
        }
      }
      if(LoRaWAN_Counter == 3)
      {
        //reset counters to restart flow
        DASH7_Counter = 0;
        LoRaWAN_Counter = 0;
      }
    }
   
    counter++; */
    //HAL_Delay(1000);
    

    /* USER CODE END WHILE */
    
    /* USER CODE BEGIN 3 */
  }
  /* USER CODE END 3 */
}

void goToSleep(void) {
  
      printf("going into sleepmode\r\n"); 
       HAL_SuspendTick(); 

      HAL_PWR_EnterSTOPMode(PWR_MAINREGULATOR_ON, PWR_SLEEPENTRY_WFI);

      HAL_ResumeTick(); 
      SystemClock_Config(); 
      printf(" came out of sleepmode \r\n");  
      timer3_first=0;  
}

//----------------------------------------------------------start send message methods--------------------------------------------------------------------------------------------

void send_message(uint8_t type) {
  if (messageMode==0) {                 //dash7mode
    switch (type) {
      case 1:
      messageCounter++;
      Dash7_send_temphum();  
      printf("sending temphum message\r\n");
      break; 
      case 2:
      messageCounter++;
      Dash7_send_allInfo();
      printf("sending allinfo message\r\n");
      break; 
      default:
      printf("No case was matched\r\n"); 
      break;  
    }
  } else {                               //lorawanmode
      LoRaWAN_send(NULL);  
      Dash7_send_temphum(); 
      printf("sending out of reach lorawan message\r\n");
  }
}



void LoRaWAN_send(void const *argument)
{
  if (murata_init)
  {
    uint8_t loraMessage[5];
    uint8_t i = 0;
    //uint16 counter to uint8 array (little endian)
    //counter (large) type byte
    loraMessage[i++] = SHTData[0];
    loraMessage[i++] = SHTData[1];
    loraMessage[i++] = 0x00;
    
    //osMutexWait(txMutexId, osWaitForever);
    if(!Murata_LoRaWAN_Send((uint8_t *)loraMessage, i))
    {
      murata_init++;
      if(murata_init == 10)
        murata_init == 0;
    }
    else
    {
      murata_init = 1;
    }
    //BLOCK TX MUTEX FOR 3s
    //osDelay(3000);
    //osMutexRelease(txMutexId);
    LoRaWAN_Counter++;
  }
  else{
    printf("murata not initialized, not sending\r\n");
  }
}


void LoRaWAN_send_self()
{
  if (murata_init)
  {
    uint8_t loraMessage[5];
    uint8_t i = 0;
    //uint16 counter to uint8 array (little endian)
    //counter (large) type byte

    //first data transfer works, but afterwards it stays in a kind of 'transmitted' loop. Find where we can reset the flag.
    loraMessage[i++] = SHTData[0];
    loraMessage[i++] = SHTData[1];
    loraMessage[i++] = LoRaWAN_Counter >> 8;
   // osMutexWait(txMutexId, osWaitForever);
    if(!Murata_LoRaWAN_Send((uint8_t *)loraMessage, i))
    {
      printf("tis ni gelukt :( ");
      murata_init++;
      if(murata_init == 10)
        murata_init == 0;
    }
    else
    {
      murata_init = 1;
    }
    //BLOCK TX MUTEX FOR 3s
    // osDelay(3000);
    // osMutexRelease(txMutexId);
    LoRaWAN_Counter++;
  }
  else{
    printf("murata not initialized, not sending\r\n");
  }
}


void Dash7_send(void const *argument)
{
  if (murata_init)
  {
    uint8_t dash7Message[5];
    uint8_t i = 0;
    //uint16 counter to uint8 array (little endian)
    //counter (large) type byte
    dash7Message[i++] = 0x14;
    dash7Message[i++] = DASH7_Counter;
    dash7Message[i++] = DASH7_Counter >> 8;
    dash7Message[i++] = 0x00;
    dash7Message[i++] = 0x00;
    dash7Message[i++] = 0x00;
    //osMutexWait(txMutexId, osWaitForever);
    if(!Murata_Dash7_Send((uint8_t *)dash7Message, i))
    {
      murata_init++;
      if(murata_init == 10)
        murata_init == 0;
    }
    else
    {
      murata_init = 1;
    }
    //BLOCK TX MUTEX FOR 3s
    //osDelay(3000);
    //osMutexRelease(txMutexId);
    DASH7_Counter++;
  }
  else{
    printf("murata not initialized, not sending\r\n");
  }
}

void Dash7_send_temphum(void const *argument)
{
  if (murata_init)
  {
    uint8_t dash7Message[5];
    uint8_t i = 0;
    //uint16 counter to uint8 array (little endian)
    //counter (large) type byte
    dash7Message[i++] = SHTData[0];
    dash7Message[i++] = SHTData[1];
    dash7Message[i++] = 0x00;
    dash7Message[i++] = messageCounter;
    dash7Message[i++] = 0x00;
    dash7Message[i++] = 0x00;
    //osMutexWait(txMutexId, osWaitForever);
    if(!Murata_Dash7_Send((uint8_t *)dash7Message, i))
    {
      murata_init++;
      if(murata_init == 10)
        murata_init == 0;
    }
    else
    {
      murata_init = 1;
    }
    //BLOCK TX MUTEX FOR 3s
    //osDelay(3000);
    //osMutexRelease(txMutexId);
    DASH7_Counter++;
  }
  else{
    printf("murata not initialized, not sending\r\n");
  }
}


void Dash7_send_allInfo(void const *argument)
{
  if (murata_init)
  {
    uint8_t dash7Message[5];
    uint8_t i = 0;
    //uint16 counter to uint8 array (little endian)
    //counter (large) type byte
    dash7Message[i++] = SHTData[0];
    dash7Message[i++] = SHTData[1];
    dash7Message[i++] = rep_counter;
    dash7Message[i++] = messageCounter;
    dash7Message[i++] = 0x00;
    dash7Message[i++] = 0x00;

    //osMutexWait(txMutexId, osWaitForever);
    if(!Murata_Dash7_Send((uint8_t *)dash7Message, i))
    {
      murata_init++;
      if(murata_init == 10)
        murata_init == 0;
    }
    else
    {
      murata_init = 1;
    }
    //BLOCK TX MUTEX FOR 3s
    //osDelay(3000);
    //osMutexRelease(txMutexId);
    DASH7_Counter++;
  }
  else{
    printf("murata not initialized, not sending\r\n");
  }
}

//----------------------------------------------------------------------end send message methods---------------------------------------------------------------------------------------

void print_temp_hum(void){
  printf("\r\n");
  printf("Temperature: %.2f °C  \r\n", SHTData[0]);
  printf("Humidity: %.2f %% \r\n", SHTData[1]);
  printf("\r\n");
}

void temp_hum_measurement(void){

  SHT31_get_temp_hum(SHTData);
  print_temp_hum();
}

void ble_callback() {
printf(tmpbuf_ble[0]); 
printf("callback 2 \r\n");
}



void vApplicationIdleHook(){
  #if LOW_POWER
    HAL_PWR_EnterSLEEPMode(PWR_MAINREGULATOR_ON, PWR_SLEEPENTRY_WFE);
  #endif
}

void printWelcome(void)
{
  printf("\r\n");
  printf("*****************************************\r\n");
  printf("Murata Dual Stack example without scheduler\r\n");
  printf("*****************************************\r\n");
  printf("\r\n");
  char UIDString[sizeof(short_UID)];
  memcpy(UIDString, &short_UID, sizeof(short_UID));
  printf("octa ID: ");
  for (const char* p = UIDString; *p; ++p)
    {
        printf("%02x", *p);
    }
  printf("\r\n\r\n");
  HAL_GPIO_TogglePin(OCTA_BLED_GPIO_Port, OCTA_BLED_Pin);
  HAL_Delay(2000);
  HAL_GPIO_TogglePin(OCTA_BLED_GPIO_Port, OCTA_BLED_Pin);
}

/* USER CODE END 4 */

//-------------------------------------------------------start interrupt handlers -----------------------------------------------------------------------------------------------------

//See platform>octa>stm32l4xx_it.c there we placed exti15_10 function to capture interrupts on one of the pins 10-15 on connector B,C,D
// (see slides of Mr weyn for the exact function name). In this function we call the "HAL_GPIO_EXTI_IRQHandler" function in the stm32l4xx_hal_gpio.c
// file. In this function the "HAL_GPIO_EXTI_Callback" is called, which we define below 
void HAL_GPIO_EXTI_Callback(uint16_t GPIO_Pin) {
  if (GPIO_Pin==GPIO_Pin_13) {
  repFlag = 1; 
  printf("interrupt accelerometer! \r\n");
  // we work with a flag so as to make sure that we don't stay in the callback for too long. This will cause disruption. 
  // the flag will call the measurement function in de while loop
  } 
}

void EXTI1_IRQHandler(void){
    //Start reps
    __HAL_GPIO_EXTI_CLEAR_IT(GPIO_PIN_1);
    printf("INTERRUPT BUTTON! \r\n");
    repMode= !repMode;
    changeAcceleroMode=1;
    //Change registers of accelero
}

void TIM2_IRQHandler( void ) {

  //printf("elapsed period \r\n");
 
  if (__HAL_TIM_GET_FLAG(&localisation_timer, TIM_IT_UPDATE) != RESET) 
  //In case other interrupts are also running
  {
  
    if (__HAL_TIM_GET_IT_SOURCE(&localisation_timer, TIM_IT_UPDATE) != RESET) {
    
    __HAL_TIM_CLEAR_IT(&localisation_timer, TIM_IT_UPDATE);
    
    
    printf("elapsed period \r\n");
    timer2flag = 1; 
    
    
    }
  
  }
 
}

void TIM3_IRQHandler( void ) {

  //printf("elapsed period \r\n");
 
  if (__HAL_TIM_GET_FLAG(&inactive_timer, TIM_IT_UPDATE) != RESET) 
  //In case other interrupts are also running
  {
  
    if (__HAL_TIM_GET_IT_SOURCE(&inactive_timer, TIM_IT_UPDATE) != RESET) {
    
    __HAL_TIM_CLEAR_IT(&inactive_timer, TIM_IT_UPDATE);
    
    if (timer3_first>0) {
    printf("elapsed period \r\n");
    timer3flag = 1; 
    
    }
    timer3_first=1; 
    }
  
  }
 
}


// UART RX CALLBACK
void HAL_UART_RxCpltCallback(UART_HandleTypeDef *huart)
{
  if (huart == &P1_UART)
  {
    Murata_rxCallback();
    murata_data_ready = 1;
  }

  if (huart == &BLE_UART) {
    printf("in callback 1\r\n");
    BLE_flag = 1; 
  }
}


//--------------------------------------------------------------------end interrupt handlers---------------------------------------------------------------------------------------------


/**
  * @brief  Period elapsed callback in non blocking mode
  * @note   This function is called  when TIM1 interrupt took place, inside
  * HAL_TIM_IRQHandler(). It makes a direct call to HAL_IncTick() to increment
  * a global variable "uwTick" used as application time base.
  * @param  htim : TIM handle
  * @retval None
  */
void HAL_TIM_PeriodElapsedCallback(TIM_HandleTypeDef *htim)
{
  /* USER CODE BEGIN Callback 0 */

  /* USER CODE END Callback 0 */
  if (htim->Instance == TIM1)
  {
    HAL_IncTick();
  }
  /* USER CODE BEGIN Callback 1 */

  /* USER CODE END Callback 1 */
}

/**
  * @brief  This function is executed in case of error occurrence.
  * @retval None
  */
void Error_Handler(void)
{
  /* USER CODE BEGIN Error_Handler_Debug */
  /* User can add his own implementation to report the HAL error return state */

  /* USER CODE END Error_Handler_Debug */
}

#ifdef USE_FULL_ASSERT
/**
  * @brief  Reports the name of the source file and the source line number
  *         where the assert_param error has occurred.
  * @param  file: pointer to the source file name
  * @param  line: assert_param error line source number
  * @retval None
  */
void assert_failed(char *file, uint32_t line)
{
  /* USER CODE BEGIN 6 */
  /* User can add his own implementation to report the file name and line number,
     tex: printf("Wrong parameters value: file %s on line %d\r\n", file, line) */
  /* USER CODE END 6 */
}
#endif /* USE_FULL_ASSERT */

/************************ (C) COPYRIGHT STMicroelectronics *****END OF FILE****/
