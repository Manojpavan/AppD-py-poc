# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
from helpers import AppD_APIs
import xml.etree.ElementTree as ET
import re
from botbuilder.dialogs import (
    ComponentDialog,
    WaterfallDialog,
    WaterfallStepContext,
    DialogTurnResult,
)
from botbuilder.dialogs.prompts import (
    TextPrompt,
    NumberPrompt,
    ChoicePrompt,
    ConfirmPrompt,
    AttachmentPrompt,
    PromptOptions,
    PromptValidatorContext,
)
from botbuilder.dialogs.choices import Choice
from botbuilder.core import MessageFactory, UserState

from data_models import UserProfile



class UserProfileDialog(ComponentDialog):
    def __init__(self, user_state: UserState):
        super(UserProfileDialog, self).__init__(UserProfileDialog.__name__)

        self.user_profile_accessor = user_state.create_property("UserProfile")

        self.add_dialog(
            WaterfallDialog(
                WaterfallDialog.__name__,
                [
                    self.transport_step,
                    self.transport_step2,
                    self.transport_step3,
                    self.transport_step4,
                    self.name_step,
                    self.name_confirm_step,
                    #self.age_step,
                    #self.picture_step,
                    #self.confirm_step,
                    #self.summary_step,
                ],
            )
        )
        self.add_dialog(TextPrompt(TextPrompt.__name__))
        # self.add_dialog(
        #     NumberPrompt(NumberPrompt.__name__, UserProfileDialog.age_prompt_validator)
        # )
        self.add_dialog(ChoicePrompt(ChoicePrompt.__name__))
        # self.add_dialog(ConfirmPrompt(ConfirmPrompt.__name__))
        # self.add_dialog(
        #     AttachmentPrompt(
        #         AttachmentPrompt.__name__, UserProfileDialog.picture_prompt_validator
        #     )
        # )

        self.initial_dialog_id = WaterfallDialog.__name__

    async def transport_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        # WaterfallStep always finishes with the end of the Waterfall or with another dialog;
        # here it is a Prompt Dialog. Running a prompt here means the next WaterfallStep will
        # be run when the users response is received.
       
        #choices_list=[Choice("Check App status"), Choice("Check DB Status"), Choice("View Dashboard")]
        return await step_context.prompt(
            ChoicePrompt.__name__,
            PromptOptions(
                prompt=MessageFactory.text("What do you want to do?"),
                choices=[Choice("Check App status"), Choice("Check DB Status"), Choice("View Dashboard")]
            ),
        )

    async def transport_step2(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        # WaterfallStep always finishes with the end of the Waterfall or with another dialog;
        # here it is a Prompt Dialog. Running a prompt here means the next WaterfallStep will
        # be run when the users response is received.
        #<a href="{}">{}</a>
        sap_executive="https://cognizant-3m.saas.appdynamics.com/controller/#/location=CDASHBOARD_DETAIL&timeRange=last_1_hour.BEFORE_NOW.-1.-1.60&mode=MODE_DASHBOARD&dashboard=4620"
        PR1_app_dashboard="https://cognizant-3m.saas.appdynamics.com/controller/#/location=CDASHBOARD_DETAIL&timeRange=last_1_hour.BEFORE_NOW.-1.-1.60&mode=MODE_DASHBOARD&dashboard=7024"
        PR1_DB_dashboard="https://cognizant-3m.saas.appdynamics.com/controller/#/location=CDASHBOARD_DETAIL&timeRange=last_1_hour.BEFORE_NOW.-1.-1.60&mode=MODE_DASHBOARD&dashboard=5084"
        dashboard_list=f"""Below are the links for major dashboards.\n\n
        Click on the links to view the dashboards.\n\n
        
        SAP Executive Dashboard - Level 0::\n{sap_executive}
            

        PR1 - Overall Summary Dashboard::\n{PR1_app_dashboard}
            

        PR1 - Database POI - Level ::\n{PR1_DB_dashboard}
            """
        #choices_list=[Choice("Check App status"), Choice("Check DB Status"), Choice("View Dashboard")]
        print(step_context.result.value)
        if(step_context.result.value=="View Dashboard"):
            await step_context.context.send_activity(
            #MessageFactory.text(manoj),
            MessageFactory.text(dashboard_list)
            
            )
            return await step_context.end_dialog()
        else:
            print("inside else")
            print(step_context.result.value)
            return await step_context.next(step_context.result.value)
            
    async def transport_step3(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        # WaterfallStep always finishes with the end of the Waterfall or with another dialog;
        # here it is a Prompt Dialog. Running a prompt here means the next WaterfallStep will
        # be run when the users response is received.
        #<a href="{}">{}</a>
        #choices_list=[Choice("Check App status"), Choice("Check DB Status"), Choice("View Dashboard")]
        if(step_context.result=="Check DB Status"):
            print(step_context.result)
            db_choices=AppD_APIs.get_db_list()
            print(type(db_choices))
            #choices=["UR5DB","UY5DB - CLM","QO1DB - MII","DO1DB-MII","UE5DB","UC6DB - CRM JAVA","UD6DB - EP","VEXDB-EWM-APAC","UI5DB","btbiq12: oracmq02: 1522","btbiq11: oracmq01: 1522","QU1DB","QU5DB","UU1DB","QE5DB","QR5DB","QE1DB","QR1DB","UE1DB","UR1DB","VOXDB","UU5DB - TM","UV5DB - SRM","UC5DB - CRM","U35DB - GTS","UA5DB - SCM","UO5DB","btbiq11: oracmq01: 1525","btbiq12: oracmq02: 1525","UL5DB - SNC","WM - btbiaq1","UP5DB - EP","UT6DB"]
            #choices=[Choice("UR5DB"), Choice("UY5DB - CLM"), Choice("QO1DB - MII"), Choice("DO1DB-MII"), Choice("UE5DB"), Choice("UC6DB - CRM JAVA"), Choice("UD6DB - EP"), Choice("VEXDB-EWM-APAC"), Choice("UI5DB"), Choice("btbiq12: oracmq02: 1522"), Choice("btbiq11: oracmq01: 1522"), Choice("QU1DB"), Choice("QU5DB"), Choice("UU1DB"), Choice("QE5DB"), Choice("QR5DB"), Choice("QE1DB"), Choice("QR1DB"), Choice("UE1DB"), Choice("UR1DB"), Choice("VOXDB"), Choice("UU5DB - TM"), Choice("UV5DB - SRM"), Choice("UC5DB - CRM"), Choice("U35DB - GTS"), Choice("UA5DB - SCM"), Choice("UO5DB"), Choice("btbiq11: oracmq01: 1525"), Choice("btbiq12: oracmq02: 1525"), Choice("UL5DB - SNC"), Choice("WM - btbiaq1"), Choice("UP5DB - EP"), Choice("UT6DB")]
            print(step_context.result)
            #choices = [Choice(x) for x in db_choices]
            #choices = [Choice(value=str(option), action=None) for option in db_choices]
            #print(db_choices)
            return await step_context.prompt(
            ChoicePrompt.__name__,
            PromptOptions(
                #TextPrompt.__name__,
                prompt=MessageFactory.text("Which DB"),
                #choices=db_choices,
                choices=[Choice("UR5DB"), Choice("UY5DB - CLM"), Choice("QO1DB - MII"), Choice("DO1DB-MII"), Choice("UE5DB"), Choice("UC6DB - CRM JAVA"), Choice("UD6DB - EP"), Choice("VEXDB-EWM-APAC"), Choice("UI5DB"), Choice("QU1DB"), Choice("QU5DB"), Choice("UU1DB"), Choice("QE5DB"), Choice("QR5DB"), Choice("QE1DB"), Choice("QR1DB"), Choice("UE1DB"), Choice("UR1DB"), Choice("VOXDB"), Choice("UU5DB - TM"), Choice("UV5DB - SRM"), Choice("UC5DB - CRM"), Choice("U35DB - GTS"), Choice("UA5DB - SCM"), Choice("UO5DB"), Choice("UL5DB - SNC"), Choice("WM - btbiaq1"), Choice("UP5DB - EP"), Choice("UT6DB")],
            ),
        )
        else:
            print("inside else")
            return await step_context.next("Check App Status")

    async def transport_step4(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        step_context.values["name"] = step_context.result
       #str selected_app=step_context.result.value
        #print(type(selected_app))
        if(step_context.result=="Check App Status"):
            print("inside else")
            return await step_context.next(step_context.result)
        else:

            message_text=AppD_APIs.violations_db(step_context.result.value)
            
            print(message_text)
            #app_id,policy_name,deepLinkUrl,severity,description=AppD_APIs.violations(step_context.values["name"])
            # We can send messages to the user at any point in the WaterfallStep.
            await step_context.context.send_activity(
                #MessageFactory.text(manoj),
                MessageFactory.text(message_text)
                
            )
            return await step_context.end_dialog()

    async def name_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        
        #step_context.values["transport"] = step_context.result.value
        
        app_choices=AppD_APIs.get_app_list()
        print(type(app_choices))
        for Choice in app_choices:
                print(Choice)
        return await step_context.prompt(
            #TextPrompt.__name__,
            ChoicePrompt.__name__,
            PromptOptions(
                prompt=MessageFactory.text("Which Application"),
                choices=app_choices,
            ),
        )
    
    async def name_confirm_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        step_context.values["name"] = step_context.result
       #str selected_app=step_context.result.value
        #print(type(selected_app))
        
        message_text=AppD_APIs.violations(step_context.result.value)
        
        print(message_text)
        #app_id,policy_name,deepLinkUrl,severity,description=AppD_APIs.violations(step_context.values["name"])
        # We can send messages to the user at any point in the WaterfallStep.
        await step_context.context.send_activity(
            #MessageFactory.text(manoj),
            MessageFactory.text(message_text)
            
        )
        return await step_context.end_dialog()
        # WaterfallStep always finishes with the end of the Waterfall or
        # with another dialog; here it is a Prompt Dialog.
    #     return await step_context.prompt(
    #          ConfirmPrompt.__name__,
    #          PromptOptions(
    #              prompt=MessageFactory.text("Would you like to give your age?")
    #          ),
    #      )

    # async def age_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
    #     if step_context.result:
    #         # User said "yes" so we will be prompting for the age.
    #         # WaterfallStep always finishes with the end of the Waterfall or with another dialog,
    #         # here it is a Prompt Dialog.
    #         return await step_context.prompt(
    #             NumberPrompt.__name__,
    #             PromptOptions(
    #                 prompt=MessageFactory.text("Please enter your age."),
    #                 retry_prompt=MessageFactory.text(
    #                     "The value entered must be greater than 0 and less than 150."
    #                 ),
    #             ),
    #         )

    #     # User said "no" so we will skip the next step. Give -1 as the age.
    #     return await step_context.next(-1)

    # async def picture_step(
    #     self, step_context: WaterfallStepContext
    # ) -> DialogTurnResult:
    #     age = step_context.result
    #     step_context.values["age"] = age

    #     msg = (
    #         "No age given."
    #         if step_context.result == -1
    #         else f"I have your age as {age}."
    #     )

    #     # We can send messages to the user at any point in the WaterfallStep.
    #     await step_context.context.send_activity(MessageFactory.text(msg))

    #     if step_context.context.activity.channel_id == "msteams":
    #         # This attachment prompt example is not designed to work for Teams attachments, so skip it in this case
    #         await step_context.context.send_activity(
    #             "Skipping attachment prompt in Teams channel..."
    #         )
    #         return await step_context.next(None)

    #     # WaterfallStep always finishes with the end of the Waterfall or with another dialog; here it is a Prompt
    #     # Dialog.
    #     prompt_options = PromptOptions(
    #         prompt=MessageFactory.text(
    #             "Please attach a profile picture (or type any message to skip)."
    #         ),
    #         retry_prompt=MessageFactory.text(
    #             "The attachment must be a jpeg/png image file."
    #         ),
    #     )
    #     return await step_context.prompt(AttachmentPrompt.__name__, prompt_options)

    # async def confirm_step(
    #     self, step_context: WaterfallStepContext
    # ) -> DialogTurnResult:
    #     step_context.values["picture"] = (
    #         None if not step_context.result else step_context.result[0]
    #     )

    #     # WaterfallStep always finishes with the end of the Waterfall or
    #     # with another dialog; here it is a Prompt Dialog.
    #     return await step_context.prompt(
    #         ConfirmPrompt.__name__,
    #         PromptOptions(prompt=MessageFactory.text("Is this ok?")),
    #     )
    
    # async def summary_step(
    #     self, step_context: WaterfallStepContext
    # ) -> DialogTurnResult:
    #     if step_context.result:
    #         # Get the current profile object from user state.  Changes to it
    #         # will saved during Bot.on_turn.
    #         user_profile = await self.user_profile_accessor.get(
    #             step_context.context, UserProfile
    #         )

    #         user_profile.transport = step_context.values["transport"]
    #         user_profile.name = step_context.values["name"]
    #         user_profile.age = step_context.values["age"]
    #         user_profile.picture = step_context.values["picture"]

    #         msg = f"I have your mode of transport as {user_profile.transport} and your name as {user_profile.name}."
    #         if user_profile.age != -1:
    #             msg += f" And age as {user_profile.age}."

    #         await step_context.context.send_activity(MessageFactory.text(msg))

    #         if user_profile.picture:
    #             await step_context.context.send_activity(
    #                 MessageFactory.attachment(
    #                     user_profile.picture, "This is your profile picture."
    #                 )
    #             )
    #         else:
    #             await step_context.context.send_activity(
    #                 "A profile picture was saved but could not be displayed here."
    #             )
    #     else:
    #         await step_context.context.send_activity(
    #             MessageFactory.text("Thanks. Your profile will not be kept.")
    #         )

    #     # WaterfallStep always finishes with the end of the Waterfall or with another
    #     # dialog, here it is the end.
    #     return await step_context.end_dialog()

    # @staticmethod
    # async def age_prompt_validator(prompt_context: PromptValidatorContext) -> bool:
    #     # This condition is our validation rule. You can also change the value at this point.
    #     return (
    #         prompt_context.recognized.succeeded
    #         and 0 < prompt_context.recognized.value < 150
    #     )

    # @staticmethod
    # async def picture_prompt_validator(prompt_context: PromptValidatorContext) -> bool:
    #     if not prompt_context.recognized.succeeded:
    #         await prompt_context.context.send_activity(
    #             "No attachments received. Proceeding without a profile picture..."
    #         )

    #         # We can return true from a validator function even if recognized.succeeded is false.
    #         return True

    #     attachments = prompt_context.recognized.value

    #     valid_images = [
    #         attachment
    #         for attachment in attachments
    #         if attachment.content_type in ["image/jpeg", "image/png"]
    #     ]

    #     prompt_context.recognized.value = valid_images

    #     # If none of the attachments are valid images, the retry prompt should be sent.
    #     return len(valid_images) > 0
