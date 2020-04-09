package org.alicebot.ab.cli;

import org.alicebot.ab.Bot;

import org.restlet.*;
import org.restlet.data.Protocol;
import org.restlet.routing.Router;

import org.alicebot.ab.Chat;
import org.alicebot.ab.utils.IOUtils;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * Created by haggais on 3/01/2016.
 */
public class Main extends Application{

    private static final Logger log = LoggerFactory.getLogger(Main.class);

    public static void main(String args[]) throws Exception{
//        String path = System.getProperty("user.dir");
//        String name = "alice2";
//        String action = "chat";
//
//        Bot bot = new Bot(name, path, action);
//        bot.brain.nodeStats();
//
//        Chat chatSession = new Chat(bot);
        
        Component server = new Component() ;
        server.getServers().add(Protocol.HTTP, 8080) ;
        server.getDefaultHost().attach(new Main()) ;
        server.start();

//        while (true) {
//            System.out.print("human: ");
//            String textLine = IOUtils.readInputTextLine();
//
//            if (textLine == null || textLine.equals("q")) {
//                bot.writeQuit();
//                System.exit(0);
//            }
//
//            String response = chatSession.multisentenceRespond(textLine);
//            System.out.println(name + ": " +  response);
//        }
    }
    
    @Override
    public Restlet createInboundRoot() {
        Router router = new Router(getContext()) ;
        router.attach( "/programab", ProgramABResource.class ) ;             
        return router;
    }
}
