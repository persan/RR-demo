with Rr_Demo.Rand_Positive;
with Ada.Text_IO;
procedure Rr_Demo.Main is
   use Ada.Text_IO;

   Generator : Rand_Positive.Generator;

   Bug   : Boolean := False;
   Value : Integer := 99;

   procedure Make_Bug (Event : Integer) is
   begin
      Value := Event;
      Bug := True;
   end Make_Bug;

   procedure Do_Bug (Event : Integer) is
      pragma Unreferenced (Event);
   begin
      if Value = 99 then
         Bug := True;
      end if;
   end Do_Bug;

   procedure Not_Fine (Event : Integer) is
   begin
      Value := Event;
      Bug := True;
   end Not_Fine;

   procedure Shit (Event : Integer) is
      pragma Unreferenced (Event);
   begin
      Bug := True;
   end Shit;

   procedure Oops (Event : Integer) is
   begin
      Value := Event + 100;
      Bug := True;
   end Oops;

begin
   declare -- Dependency on externals
      F : File_Type;
      procedure Dummy (D : String) is
      begin
         null;
      end Dummy;
   begin
      Open (F, In_File, "dummy.txt");
      Dummy (Get_Line (F));
      Close (F);
   end;

   Rand_Positive.Reset (Generator);

   for I in 1 .. 10 loop
      if
        Rand_Positive.Random (Generator) < (Positive'Last / 1000) -- Probability of bug per run
      then
         case Rand_Positive.Random (Generator) mod 5 is -- Which bug ?
            when 0 => Make_Bug (I);
            when 1 => Do_Bug (I);
            when 3 => Not_Fine (I);
            when 4 => Shit (I);
            when others => Oops (I);
         end case;
      end if;
   end loop;

   if Bug then
      raise Error;
   end if;

end Rr_Demo.Main;
