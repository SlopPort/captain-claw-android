package pl.pazur.port;

import android.app.Activity;
import android.app.AlertDialog;
import android.content.SharedPreferences;
import android.widget.*;

/** LLM-authored adaptation: persistent controls and damage/healing presets. */
final class GameplaySettingsUi {
    static SharedPreferences prefs(Activity a){return a.getSharedPreferences("controls",Activity.MODE_PRIVATE);}
    static void save(Activity a,String key,int value) {
        if(!prefs(a).edit().putInt(key,value).commit())
            new AlertDialog.Builder(a).setMessage(R.string.settings_save_error).setPositiveButton("OK",null).show();
    }
    static void choices(Activity a,LinearLayout parent,int title,int names,String key,int fallback,int base) {
        TextView heading=new TextView(a);heading.setText(title);heading.setTextSize(20);parent.addView(heading);
        RadioGroup group=new RadioGroup(a);String[] labels=a.getResources().getStringArray(names);
        for(int i=0;i<labels.length;i++){RadioButton row=new RadioButton(a);row.setId(base+i);row.setText(labels[i]);group.addView(row);}
        int selected=prefs(a).getInt(key,fallback);
        group.check(base+(selected>=0&&selected<labels.length?selected:fallback));
        group.setOnCheckedChangeListener((g,id)->save(a,key,id-base));parent.addView(group);
    }
    static void slider(Activity a,LinearLayout parent,String label,String key,int initial,int min,int max,int id) {
        TextView caption=new TextView(a);parent.addView(caption);
        SeekBar bar=new SeekBar(a);bar.setId(id);bar.setMax(max-min);
        int current=Math.max(min,Math.min(max,prefs(a).getInt(key,initial)));
        bar.setProgress(current-min);caption.setText(label+": "+current);parent.addView(bar);
        bar.setOnSeekBarChangeListener(new SeekBar.OnSeekBarChangeListener(){
            public void onStartTrackingTouch(SeekBar b){}
            public void onProgressChanged(SeekBar b,int value,boolean user){caption.setText(label+": "+(value+min));}
            public void onStopTrackingTouch(SeekBar b){save(a,key,b.getProgress()+min);}
        });
    }
    static void difficulty(Activity a,LinearLayout parent) {
        choices(a,parent,R.string.difficulty_title,R.array.difficulty_names,"difficulty",1,2100);
        TextView help=new TextView(a);help.setText(R.string.difficulty_help);parent.addView(help);
    }
    static void controls(Activity a,LinearLayout parent) {
        choices(a,parent,R.string.movement_title,R.array.movement_names,"movement",0,2200);
        slider(a,parent,a.getString(R.string.deadzone),"deadzone",14,8,28,2300);
        TextView help=new TextView(a);help.setText(R.string.deadzone_help);parent.addView(help);
        Button editor=new Button(a);editor.setId(2301);editor.setText(R.string.edit_touch_buttons);
        editor.setOnClickListener(v->edit(a));parent.addView(editor);
    }
    static AlertDialog edit(Activity a) {
        ScrollView scroll=new ScrollView(a);LinearLayout body=new LinearLayout(a);body.setOrientation(LinearLayout.VERTICAL);scroll.addView(body);
        TextView help=new TextView(a);help.setText(R.string.button_editor_help);body.addView(help);
        Spinner button=new Spinner(a);
        button.setAdapter(new ArrayAdapter<String>(a,android.R.layout.simple_spinner_dropdown_item,a.getResources().getStringArray(R.array.touch_button_names)));
        body.addView(button);
        LinearLayout sliders=new LinearLayout(a);sliders.setOrientation(LinearLayout.VERTICAL);body.addView(sliders);
        Runnable refresh=()->{
            sliders.removeAllViews();int i=button.getSelectedItemPosition();
            slider(a,sliders,a.getString(R.string.button_size),"button_size_"+i,100,60,130,2400);
            slider(a,sliders,a.getString(R.string.button_x),"button_x_"+i,0,-100,100,2401);
            slider(a,sliders,a.getString(R.string.button_y),"button_y_"+i,0,-100,100,2402);
        };
        button.setOnItemSelectedListener(new android.widget.AdapterView.OnItemSelectedListener(){
            public void onItemSelected(android.widget.AdapterView<?> p,android.view.View v,int n,long id){refresh.run();}
            public void onNothingSelected(android.widget.AdapterView<?> p){}
        });refresh.run();
        Button reset=new Button(a);reset.setText(R.string.reset_touch_buttons);body.addView(reset);
        reset.setOnClickListener(v->{
            SharedPreferences.Editor editor=prefs(a).edit();
            for(int i=0;i<5;i++)editor.remove("button_size_"+i).remove("button_x_"+i).remove("button_y_"+i);
            if(!editor.commit())new AlertDialog.Builder(a).setMessage(R.string.settings_save_error).setPositiveButton("OK",null).show();
            refresh.run();
        });
        return new AlertDialog.Builder(a).setTitle(R.string.edit_touch_buttons).setView(scroll).setPositiveButton(android.R.string.ok,null).show();
    }
}
