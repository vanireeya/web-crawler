package org.alicebot.ab.cli;

import org.alicebot.ab.Bot;
import org.alicebot.ab.Chat;
import org.json.* ;
import org.restlet.representation.* ;
import org.restlet.ext.*;
import org.restlet.ext.json.JsonRepresentation;
import org.restlet.resource.* ;
import org.restlet.data.* ;

import java.io.IOException ;
import java.util.Collection ;


public class ProgramABResource extends ServerResource {
	
	@Get
    public Representation get_action() throws Exception {
		setStatus( org.restlet.data.Status.SUCCESS_OK ) ;
        return new StringRepresentation("Get request working") ;           
    }
	
	@Post
    public Representation post_action (Representation rep) throws IOException, JSONException {
		
		JsonRepresentation request_body = new JsonRepresentation(rep);
        JSONObject jsonobject = request_body.getJsonObject();
        
        String incoming_question = jsonobject.getString("question");
        System.out.println("The incoming question is : " + incoming_question);
		        
        String path = System.getProperty("user.dir");
        String name = "alice2";
        String action = "chat";

        Bot bot = new Bot(name, path, action);
        bot.brain.nodeStats();

        Chat chatSession = new Chat(bot);
        
        String response = chatSession.multisentenceRespond(incoming_question);
        
        System.out.println("->->->->->-> "+name + ": " +  response);
        setStatus( org.restlet.data.Status.SUCCESS_OK ) ;
        return new StringRepresentation(response) ;	
	}
	

}
