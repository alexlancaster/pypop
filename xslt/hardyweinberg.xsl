<xsl:stylesheet 
 version='1.0'
 xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
 xmlns:data="any-uri">

 <!-- boiler-plate text that we may want to re-use -->
 <data:hardyweinberg-col-headers>
  <text>Observed</text>
  <text>Expected</text>
  <text>Chi-square</text>
  <text colwidth="5">dof</text>
  <text justify="left">p-value</text>
 </data:hardyweinberg-col-headers>

 <!-- ################  HARDY-WEINBERG STATISTICS ###################### --> 

 <xsl:template match="hardyweinberg">
  <xsl:call-template name="section">
   <xsl:with-param name="title">
    <xsl:call-template name="locus-header">
     <xsl:with-param name="title">HardyWeinberg</xsl:with-param>
    </xsl:call-template>
   </xsl:with-param>
   <xsl:with-param name="level" select="2"/>
   <xsl:with-param name="text">

    <!-- do genotype table -->
    <xsl:apply-templates select="genotypetable"/>
    
    <xsl:call-template name="newline"/>
    
    <!-- indent first line of table -->
    <xsl:call-template name="prepend-pad">
     <xsl:with-param name="length" select="$hardyweinberg-first-col-width"/>
    </xsl:call-template>
    
    <!-- print header for the individual stats -->
    <xsl:for-each select="document('')//data:hardyweinberg-col-headers/text">
     <xsl:variable name="width">
      <xsl:choose>
       <xsl:when test="@colwidth">
	<xsl:value-of select="@colwidth"/>
       </xsl:when>
       <xsl:otherwise> 
	<xsl:value-of select="$hardyweinberg-col-width"/>
       </xsl:otherwise>
      </xsl:choose>
     </xsl:variable>
     <xsl:choose>
      <xsl:when test="@justify='left'">
       <xsl:text> </xsl:text>
       <xsl:call-template name="append-pad">
	<xsl:with-param name="padVar" select="."/>
	<xsl:with-param name="length" select="$width"/>
       </xsl:call-template>
      </xsl:when>
      <xsl:otherwise>
       <xsl:call-template name="prepend-pad">
	<xsl:with-param name="padVar" select="."/>
	<xsl:with-param name="length" select="$width"/>
       </xsl:call-template>
      </xsl:otherwise>
     </xsl:choose>
    </xsl:for-each>
    
    <!-- separator -->
    <xsl:call-template name="newline"/>
    <xsl:call-template name="separator"/>
    <xsl:call-template name="newline"/>
    
    <!-- no do individual stats for each class -->
    <xsl:apply-templates select="common"/>
    <xsl:apply-templates select="lumped"/>
    <xsl:apply-templates select="commonpluslumped"/>
    <xsl:apply-templates select="heterozygotes|homozygotes"/>
    
    <!-- do stats for all the heterozygotes and genotypes -->
    <xsl:apply-templates select="heterozygotesByAllele"/>
    
    <xsl:apply-templates select="genotypetable" mode="genotypesByGenotype"/>
 
   </xsl:with-param>
  </xsl:call-template>
 </xsl:template>
 
 <!-- template to generate the (padded) cell ;-) -->
 <!-- this also handles the case when there is no tag because it -->
 <!-- will simply return a white-space padded cell of the right length -->
 <xsl:template name="hardyweinberg-gen-cell">
  <xsl:param name="node" select="."/>
  <xsl:param name="width" select="$hardyweinberg-col-width"/>

  <!-- some columns may be left-justified, set this param to '0' if desired -->
  <xsl:param name="prepend" select="1"/>
  
  <xsl:choose>
   <xsl:when test="$prepend=1">
    <xsl:call-template name="prepend-pad">
     <xsl:with-param name="padVar" select="$node"/>
     <xsl:with-param name="length" select="$width"/>
    </xsl:call-template>
   </xsl:when>
   <xsl:otherwise>
    <!-- make sure there is at least one initial space -->
    <!-- FIXME: this entire table generation system is getting way too -->
    <!-- kludgy, need to replace the entire system, with a clean, generic --> 
    <!-- system real soon now(TM) -->
    <xsl:text> </xsl:text>
    <xsl:call-template name="append-pad">
     <xsl:with-param name="padVar" select="$node"/>
     <xsl:with-param name="length" select="$width"/>
    </xsl:call-template>
   </xsl:otherwise>
  </xsl:choose>
 </xsl:template>

 <!-- template to generate the row -->
 <xsl:template name="hardyweinberg-gen-row">
  
  <!-- create variables from the contents of the cells  -->
  <xsl:variable name="observed">
   <xsl:call-template name="hardyweinberg-gen-cell">
    <xsl:with-param name="node" select="observed"/>
   </xsl:call-template>
  </xsl:variable>
  <xsl:variable name="expected">
   <!-- for this column only, round the expected to 2 decimal places -->
   <xsl:variable name="expected-rounded">
    <xsl:call-template name="round-to">
     <xsl:with-param name="node" select="expected"/>
     <xsl:with-param name="places" select="2"/>
    </xsl:call-template>
   </xsl:variable>
   <!-- then pass this new value to the generate the table cell -->
   <xsl:call-template name="hardyweinberg-gen-cell">
    <xsl:with-param name="node" select="$expected-rounded"/>
   </xsl:call-template>
  </xsl:variable>
  <xsl:variable name="chisq">
   <xsl:call-template name="hardyweinberg-gen-cell">
    <xsl:with-param name="node" select="chisq"/>
   </xsl:call-template>
  </xsl:variable>
  <xsl:variable name="pvalue">
   <xsl:call-template name="hardyweinberg-gen-cell">
    <xsl:with-param name="node">
     <xsl:apply-templates select="pvalue"/>
    </xsl:with-param>
    <xsl:with-param name="prepend" select="0"/>
   </xsl:call-template>
  </xsl:variable>
  <xsl:variable name="chisqdf">
   <xsl:call-template name="hardyweinberg-gen-cell">
    <xsl:with-param name="node" select="chisqdf"/>
    <xsl:with-param name="width" select="5"/>
   </xsl:call-template>
  </xsl:variable>

  <!-- concatenate all the cells -->
  <xsl:value-of select="concat($observed,$expected,$chisq,$chisqdf,$pvalue)"/>

 </xsl:template>

 <!-- print out overall HW stats  -->
 <xsl:template match="common|lumped|commonpluslumped|heterozygotes|homozygotes">

 <xsl:variable name="type">
   <xsl:choose>
    <xsl:when test="name(.)='homozygotes'">All homozygotes</xsl:when>
    <xsl:when test="name(.)='heterozygotes'">All heterozygotes</xsl:when>
    <xsl:when test="name(.)='common'">Common</xsl:when>
    <xsl:when test="name(.)='commonpluslumped'">Common + lumped</xsl:when>
    <xsl:when test="name(.)='lumped'">Lumped genotypes</xsl:when>
    <xsl:otherwise>
     <xsl:message terminate="yes">Should always match something</xsl:message>
    </xsl:otherwise>
   </xsl:choose>
 </xsl:variable>


  <!-- indent table -->
  <xsl:call-template name="prepend-pad">
   <xsl:with-param name="length" select="$hardyweinberg-first-col-width"/>
   <xsl:with-param name="padVar" select="$type"/>
  </xsl:call-template>
  
  <xsl:choose>
   
   <xsl:when test="*!=''">
    <!-- when the tag has content generate the row -->
    <xsl:call-template name="hardyweinberg-gen-row"/>
   </xsl:when>

   <!-- if the tag does not have content, generate a diagnostic message -->
   <!-- based on the 'role' attribute -->
   <xsl:when test="*=''">

    <!-- make an extra space, for case when following text is flush left -->
    <xsl:text> </xsl:text>
  
    <xsl:choose>
     <xsl:when test="@role='too-many-parameters'">
      <xsl:text>Too many parameters for chi-square test.</xsl:text>
     </xsl:when>
     <xsl:when test="@role='no-common-genotypes'">
      <xsl:text>No commmon genotypes; chi-square cannot be calculated</xsl:text>
     </xsl:when>
     <xsl:when test="@role='no-rare-genotypes'">
      <xsl:text>No rare genotypes observed.</xsl:text>
     </xsl:when>
     <xsl:when test="@role='too-few-expected'">
      <xsl:text>
       The total number of expected genotypes is less than </xsl:text><xsl:value-of
       select="../lumpBelow"/>
     </xsl:when>
     <xsl:when test="@role='not-calculated'">
      <xsl:text>Value not calculated.</xsl:text>
     </xsl:when>
     <xsl:when test="@role='huh'">
      <xsl:text>Unhandled logical path through Hardy-Weinberg.</xsl:text>
     </xsl:when>
     <xsl:otherwise>
      <xsl:text>Condition: </xsl:text><xsl:value-of
       select="@role"/><xsl:text> not recognized.</xsl:text>
     </xsl:otherwise>
    </xsl:choose>
    <xsl:call-template name="newline"/>
   </xsl:when>

   <!-- an "assert" message to test XSLT is working -->
   <xsl:otherwise>
    <xsl:message>Error! Output XML condition not covered!</xsl:message>
   </xsl:otherwise>
  </xsl:choose>
  <xsl:call-template name="newline"/>

  <!-- separator -->
  <xsl:call-template name="separator"/>
  <xsl:call-template name="newline"/>

 </xsl:template>

 <!-- print out info on heterozygotes and genotypes -->
 <xsl:template match="heterozygotesByAllele">
  <xsl:text>Heterozygotes by allele</xsl:text>
  <xsl:call-template name="newline"/>
  <xsl:for-each select="allele">
   
   <!-- sort by allele name -->
   <xsl:sort select="@name" data-type="text"/>
   <!-- indent table with name of the allele -->
   <xsl:call-template name="prepend-pad">
    <xsl:with-param name="length" select="$hardyweinberg-first-col-width"/>
    <xsl:with-param name="padVar" select="@name"/>
   </xsl:call-template>
   <!-- generate the row -->
   <xsl:call-template name="hardyweinberg-gen-row"/>
   <xsl:call-template name="newline"/>
  </xsl:for-each>  

  <xsl:call-template name="newline"/>
  
  <!-- separator -->
  <xsl:call-template name="separator"/>
  <xsl:call-template name="newline"/>

 </xsl:template>

 <!-- format genotype table for HW -->
 <xsl:template match="genotypetable" mode="genotypesByGenotype">
  <xsl:text>Genotypes by genotype</xsl:text>
  <xsl:call-template name="newline"/>

  <xsl:for-each select="genotype[chisq/@role!='not-calculated']">  
   <xsl:sort select="@col" data-type="text"/>
   <!-- generate genotype name -->
   <xsl:variable name="name">
    <xsl:value-of select="@col"/>:<xsl:value-of select="@row"/> 
   </xsl:variable>

  <!-- indent table with name of the genotype -->
   <xsl:call-template name="prepend-pad">
    <xsl:with-param name="length" select="$hardyweinberg-first-col-width"/>
    <xsl:with-param name="padVar" select="$name"/>
   </xsl:call-template>
   <!-- generate the row -->
   <xsl:call-template name="hardyweinberg-gen-row"/>
   <xsl:call-template name="newline"/>
  </xsl:for-each>

  <!-- generate totals at end of table -->
  <xsl:call-template name="prepend-pad">
   <xsl:with-param name="length" select="$hardyweinberg-first-col-width"/>
   <xsl:with-param name="padVar" select="'Total'"/>
  </xsl:call-template>

  <xsl:call-template name="hardyweinberg-gen-cell">
   <xsl:with-param name="node" select="sum(genotype[chisq/@role!='not-calculated']/observed)"/>
  </xsl:call-template>
  <xsl:call-template name="hardyweinberg-gen-cell">
   <xsl:with-param name="node" select="sum(genotype[chisq/@role!='not-calculated']/expected)"/>
  </xsl:call-template>
  <xsl:call-template name="newline"/>

  <!-- separator -->
  <xsl:call-template name="separator"/>
  <xsl:call-template name="newline"/>

 </xsl:template>

 <!-- format genotype table for HW -->
 <xsl:template match="genotypetable">

  <xsl:text>Table of genotypes, format of each cell is: observed/expected.</xsl:text>
  <xsl:call-template name="newline"/>

  <!-- save the unique list of column names-->
  <xsl:variable name="unique-cols" select="genotype[@col!=preceding-sibling::genotype/@col]/@col"/>

  <!-- save the current node -->
  <xsl:variable name="curr-node" select="."/>

  <xsl:variable name="row-len-max">
   <xsl:call-template name="max-string-len">
    <xsl:with-param name="path" select="genotype/@row"/>
   </xsl:call-template>
  </xsl:variable>

  <!-- find the longest observed value -->
  <xsl:variable name="observed-max">
   <xsl:call-template name="max-string-len">
    <xsl:with-param name="path" select="genotype/observed"/>
   </xsl:call-template>
  </xsl:variable>

  <!-- calculate the  width required for each cell, this twice the maximum -->
  <!-- length of the "observed" cell 'XXX'  plus space needed for chars  -->
  <!-- e.g.:  XXX/XXX.0 and a padding space  -->
  <xsl:variable name="cell-width-max" select="$observed-max * 2 + 4"/>

  <!-- choose the greater of the allele name or cell-width-max for the -->
  <!-- standard width -->
  <xsl:variable name="width">
   <xsl:choose>
    <xsl:when test="$cell-width-max &gt; $row-len-max">
     <xsl:value-of select="$cell-width-max"/>
    </xsl:when>
    <xsl:otherwise>
     <xsl:value-of select="$row-len-max"/>
    </xsl:otherwise>
   </xsl:choose>
  </xsl:variable>

  <!-- calculate the number of cols to fit (subtract one for the row -->
  <!-- allele names) -->
  <xsl:variable name="hardyweinberg-cols-to-fit" 
   select="floor($page-width div $width) - 1"/>

  <!-- check each unique column and output a subtable whenever  -->
  <!-- the column header is a multiple of the cols to fit on the page -->
  <xsl:for-each select="$unique-cols">

   <xsl:variable name="pos" select="position()"/>

   <xsl:choose>
    <!-- can fit the max number of cols on page -->
    <xsl:when test="$pos mod $hardyweinberg-cols-to-fit = 0">

     <xsl:variable name="end-col" select="position()"/>
     <xsl:variable name="start-col" 
      select="$end-col - $hardyweinberg-cols-to-fit + 1"/>

     <xsl:call-template name="gen-subtable">
      <xsl:with-param name="node" select="$curr-node"/>
      <xsl:with-param name="start-col" select="$start-col"/>
      <xsl:with-param name="end-col" select="$end-col"/>
      <xsl:with-param name="unique-cols" select="$unique-cols"/>
      <xsl:with-param name="row-len-max" select="$row-len-max"/>
      <xsl:with-param name="col-len-max" select="$width"/>
     </xsl:call-template>

     <xsl:text>                             [Cols: </xsl:text>
     <xsl:value-of select="$start-col"/><xsl:text> to </xsl:text>
     <xsl:value-of select="$end-col"/><xsl:text>]</xsl:text>

    </xsl:when>

    <!-- this deals with the situtation when there are some leftover cols -->
    <xsl:when test="$pos=last() and $pos mod $hardyweinberg-cols-to-fit != 0">
     
     <xsl:variable name="end-col" select="position()"/>
     <xsl:variable name="start-col" 
      select="$end-col - ($pos mod $hardyweinberg-cols-to-fit) + 1"/>

     <xsl:call-template name="gen-subtable">
      <xsl:with-param name="node" select="$curr-node"/>
      <xsl:with-param name="start-col" select="$start-col"/>
      <xsl:with-param name="end-col" select="$end-col"/>
      <xsl:with-param name="unique-cols" select="$unique-cols"/>
      <xsl:with-param name="row-len-max" select="$row-len-max"/>
      <xsl:with-param name="col-len-max" select="$width"/>
     </xsl:call-template>

     <xsl:text>                             [Cols: </xsl:text>
     <xsl:value-of select="$start-col"/><xsl:text> to </xsl:text>
     <xsl:value-of select="$end-col"/><xsl:text>]</xsl:text>

    </xsl:when>
   </xsl:choose>

  </xsl:for-each>

  <xsl:call-template name="newline"/>
 </xsl:template>

 <xsl:template name="gen-subtable">
  <xsl:param name="node"/>
  <xsl:param name="start-col"/>
  <xsl:param name="end-col"/>
  <xsl:param name="unique-cols"/>
  <xsl:param name="row-len-max"/>
  <xsl:param name="col-len-max"/>
  
  <xsl:for-each select="$node/genotype">
   <xsl:sort select="@row"/>
   
   <xsl:variable name="row" select="@row"/>
   <xsl:variable name="col" select="@col"/>
   
   <!-- generate row name, only on first col and only if the row --> 
   <!-- is part of this column processing -->
   
   <xsl:if test="@row!=preceding-sibling::genotype/@row and $unique-cols[.=$row and position() &gt;= $start-col]">
    <xsl:call-template name="newline"/>
    <xsl:call-template name="prepend-pad">
     <xsl:with-param name="length" select="$row-len-max"/>
     <xsl:with-param name="padVar" select="@row"/>
    </xsl:call-template>
   </xsl:if>

   <!-- only output cell if in the current column range -->
   <xsl:if test="$unique-cols[.=$col and position() &gt;= $start-col and position() &lt;= $end-col]"> 

    <xsl:variable name="cell">
     <!-- round and format the decimal values of "observed" to nearest 0.1 -->
     <xsl:value-of select="observed"/><xsl:text>/</xsl:text>
     <xsl:call-template name="round-to">
      <xsl:with-param name="node" select="expected"/>
      <xsl:with-param name="places" select="1"/>
     </xsl:call-template>
    </xsl:variable>
    
    <!-- output cell with padding -->
    <xsl:call-template name="prepend-pad">
     <xsl:with-param name="length" select="$col-len-max"/>
     <xsl:with-param name="padVar" select="$cell"/> 
    </xsl:call-template>
    
   </xsl:if>
    
  </xsl:for-each>

  <xsl:call-template name="newline"/>

  <!-- indent row for column names-->
  <xsl:call-template name="prepend-pad">
   <xsl:with-param name="length" select="$row-len-max"/>
  </xsl:call-template>
  
  <!-- create column footer by filtering out appropriate columns from
  unique column list -->
  <xsl:for-each select="$unique-cols[position() &gt;= $start-col and position() &lt;= $end-col]">
   <xsl:sort select="."/>
   <xsl:call-template name="prepend-pad">
    <xsl:with-param name="length" select="$col-len-max"/>
    <xsl:with-param name="padVar" select="."/>
   </xsl:call-template>
  </xsl:for-each>

  <xsl:call-template name="newline"/>

 </xsl:template>

 <!-- print out Guo and Thompson output if it's generated -->
 <xsl:template match="hardyweinbergGuoThompson">
  <xsl:call-template name="section">
   <xsl:with-param name="title">
    <xsl:call-template name="locus-header">
     <xsl:with-param name="title">Guo and Thompson HardyWeinberg output</xsl:with-param>
    </xsl:call-template>
   </xsl:with-param>
   <xsl:with-param name="level" select="2"/>
   <xsl:with-param name="text">
    <xsl:choose>
     <xsl:when test="@role='too-few-alleles'">
      <xsl:text>Too few alleles</xsl:text>
     </xsl:when>
     <xsl:when test="@role='too-large-matrix'">
      <xsl:text>Too large a matrix for Guo and Thompson</xsl:text>
     </xsl:when>
     
     <xsl:otherwise>
      <xsl:choose>
       <!-- only when 1 is produced as a pvalue, we return an error -->
       <xsl:when test="normalize-space(pvalue)='1'">
	<xsl:text>Guo and Thompson test failed to converge.</xsl:text>
       </xsl:when>
       <xsl:otherwise>
	<xsl:call-template name="linesep-fields">
	 <xsl:with-param name="nodes" select="pvalue|stderr|dememorizationSteps|samplingNum|samplingSize"/>
	</xsl:call-template>
       </xsl:otherwise>
      </xsl:choose>
      <!--
      <xsl:text>*switches*</xsl:text>
      <xsl:call-template name="newline"/>
      <xsl:call-template name="linesep-fields">
      <xsl:with-param name="nodes" select="switches/*"/>
     </xsl:call-template>
      -->
     </xsl:otherwise>
     
    </xsl:choose>
   </xsl:with-param>
  </xsl:call-template>
 </xsl:template>

 <!-- ################  END HARDY-WEINBERG STATISTICS  ############### --> 

</xsl:stylesheet>
<!-- 
Local variables:
mode: xml
sgml-default-dtd-file: "xsl.ced"
sgml-indent-step: 1
sgml-indent-data: 1
End:
-->
 